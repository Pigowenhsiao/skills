from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx
import yaml
from graphify.analyze import god_nodes, suggest_questions, surprising_connections
from graphify.benchmark import run_benchmark
from graphify.cluster import cluster, score_all
from graphify.detect import detect
from graphify.export import to_html, to_json
from graphify.manifest import save_manifest
from graphify.report import generate


VAULT_DIR = Path(r"C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian")
OUT_DIR = VAULT_DIR / "graphify-out"
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def file_node_id(rel: str) -> str:
    return f"file:{rel}"


def concept_node_id(kind: str, value: str) -> str:
    return f"{kind}:{value}"


def best_title(path: Path, text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return normalize(line[2:])
    return path.stem


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        return {}


def strip_frontmatter(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return text
    return text[match.end() :]


def resolve_link(target: str, current_rel: str, md_lookup: dict[str, str], basename_lookup: dict[str, list[str]]) -> str | None:
    target = target.replace("\\", "/").strip()
    target = target[:-3] if target.lower().endswith(".md") else target
    current_parent = str(Path(current_rel).parent).replace("\\", "/")
    candidates = []
    if "/" in target:
        candidates.append(f"{target}.md")
    else:
        if current_parent not in {".", ""}:
            candidates.append(f"{current_parent}/{target}.md")
        candidates.append(f"{target}.md")

    for candidate in candidates:
        if candidate in md_lookup:
            return md_lookup[candidate]

    base = Path(target).name.lower()
    matches = basename_lookup.get(base, [])
    if len(matches) == 1:
        return matches[0]
    return None


def community_label(G: nx.Graph, node_ids: list[str]) -> str:
    folder_terms: list[str] = []
    tag_terms: list[str] = []
    issue_terms: list[str] = []
    title_terms: list[str] = []
    for node_id in node_ids:
        data = G.nodes[node_id]
        node_type = data.get("node_type")
        label = data.get("label", "")
        if node_type == "folder":
            folder_terms.append(label)
        elif node_type == "tag":
            tag_terms.append(label)
        elif node_type == "issue":
            issue_terms.append(label)
        else:
            title_terms.append(label)
    if issue_terms:
        return Counter(issue_terms).most_common(1)[0][0]
    if tag_terms:
        return Counter(tag_terms).most_common(1)[0][0]
    if folder_terms:
        return Counter(folder_terms).most_common(1)[0][0]
    if title_terms:
        return Counter(title_terms).most_common(1)[0][0]
    return "Community"


def build_graph() -> tuple[nx.Graph, dict]:
    detection = detect(VAULT_DIR)
    files = detection.get("files", {})
    docs = [Path(p) for p in files.get("document", []) if Path(p).suffix.lower() == ".md"]
    images = [Path(p) for p in files.get("image", [])]
    papers = [Path(p) for p in files.get("paper", [])]

    G = nx.Graph()
    G.graph["hyperedges"] = []

    md_lookup: dict[str, str] = {}
    basename_lookup: dict[str, list[str]] = defaultdict(list)
    note_cache: dict[str, tuple[Path, str]] = {}

    for path in docs:
        rel = str(path.relative_to(VAULT_DIR)).replace("\\", "/")
        md_lookup[rel] = rel
        basename_lookup[path.stem.lower()].append(rel)
        try:
            note_cache[rel] = (path, path.read_text(encoding="utf-8"))
        except Exception:
            continue

    for rel, (path, text) in note_cache.items():
        title = best_title(path, text)
        node_id = file_node_id(rel)
        G.add_node(
            node_id,
            label=title,
            source_file=rel,
            file_type="document",
            node_type="file",
        )

        parts = Path(rel).parts[:-1]
        folder_chain = []
        for part in parts[:3]:
            folder_chain.append(part)
            folder_rel = "/".join(folder_chain)
            folder_id = concept_node_id("folder", folder_rel)
            G.add_node(folder_id, label=folder_rel, node_type="folder", file_type="concept")
            G.add_edge(node_id, folder_id, relation="in_folder", confidence="EXTRACTED")

        frontmatter = parse_frontmatter(text)
        tags = frontmatter.get("tags", []) or []
        if isinstance(tags, str):
            tags = [tags]
        for tag in tags:
            tag = normalize(str(tag))
            if not tag:
                continue
            tag_id = concept_node_id("tag", tag.lower())
            G.add_node(tag_id, label=tag, node_type="tag", file_type="concept")
            G.add_edge(node_id, tag_id, relation="tagged", confidence="EXTRACTED")

        for key in ("workspace", "team", "type", "company"):
            value = frontmatter.get(key)
            if not value:
                continue
            value = normalize(str(value))
            concept_id = concept_node_id(key, value.lower())
            G.add_node(concept_id, label=value, node_type=key, file_type="concept")
            G.add_edge(node_id, concept_id, relation=key, confidence="EXTRACTED")

        if rel.startswith("Lumentum/Issues/RMA Keys/"):
            issue_id = concept_node_id("issue", title.lower())
            G.add_node(issue_id, label=title, node_type="issue", file_type="concept")
            G.add_edge(node_id, issue_id, relation="defines_issue", confidence="EXTRACTED")

        if rel.startswith("Lumentum/Customers/Keys/"):
            customer_id = concept_node_id("customer", title.lower())
            G.add_node(customer_id, label=title, node_type="customer", file_type="concept")
            G.add_edge(node_id, customer_id, relation="defines_customer", confidence="EXTRACTED")

    for rel, (_, text) in note_cache.items():
        node_id = file_node_id(rel)
        body = strip_frontmatter(text)
        for match in WIKILINK_RE.finditer(body):
            target = match.group(1)
            resolved = resolve_link(target, rel, md_lookup, basename_lookup)
            if not resolved:
                continue
            G.add_edge(node_id, file_node_id(resolved), relation="wikilink", confidence="EXTRACTED")

    for path in images + papers:
        rel = str(path.relative_to(VAULT_DIR)).replace("\\", "/")
        node_id = file_node_id(rel)
        label = path.stem
        file_type = "image" if path in images else "paper"
        G.add_node(
            node_id,
            label=label,
            source_file=rel,
            file_type=file_type,
            node_type="file",
        )
        parts = Path(rel).parts[:-1]
        folder_chain = []
        for part in parts[:3]:
            folder_chain.append(part)
            folder_rel = "/".join(folder_chain)
            folder_id = concept_node_id("folder", folder_rel)
            G.add_node(folder_id, label=folder_rel, node_type="folder", file_type="concept")
            G.add_edge(node_id, folder_id, relation="in_folder", confidence="EXTRACTED")

    return G, detection


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    G, detection = build_graph()
    communities = cluster(G)
    community_labels = {cid: community_label(G, nodes) for cid, nodes in communities.items()}
    cohesion_scores = score_all(G, communities)
    god_node_list = god_nodes(G)
    surprise_list = surprising_connections(G, communities)
    question_list = suggest_questions(G, communities, community_labels)

    graph_json_path = OUT_DIR / "graph.json"
    graph_html_path = OUT_DIR / "graph.html"
    report_path = OUT_DIR / "GRAPH_REPORT.md"
    benchmark_path = OUT_DIR / "benchmark.json"
    labels_path = OUT_DIR / "community_labels.json"
    cost_path = OUT_DIR / "cost.json"
    manifest_path = OUT_DIR / "manifest.json"

    to_json(G, communities, str(graph_json_path))
    to_html(G, communities, str(graph_html_path), community_labels)

    cost = {
        "input_tokens": 0,
        "output_tokens": 0,
        "pipeline": "markdown-wikilink-refresh",
    }
    report_text = generate(
        G,
        communities,
        cohesion_scores,
        community_labels,
        god_node_list,
        surprise_list,
        detection,
        cost,
        str(VAULT_DIR),
        question_list,
    )
    report_path.write_text(report_text, encoding="utf-8")

    labels_path.write_text(json.dumps(community_labels, indent=2, ensure_ascii=False), encoding="utf-8")
    cost_path.write_text(json.dumps(cost, indent=2, ensure_ascii=False), encoding="utf-8")
    save_manifest(detection.get("files", {}), str(manifest_path))

    benchmark = run_benchmark(str(graph_json_path), corpus_words=detection.get("total_words"))
    benchmark_path.write_text(json.dumps(benchmark, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"NODES={G.number_of_nodes()}")
    print(f"EDGES={G.number_of_edges()}")
    print(f"COMMUNITIES={len(communities)}")
    print(f"TOTAL_FILES={detection.get('total_files')}")
    print(f"TOTAL_WORDS={detection.get('total_words')}")


if __name__ == "__main__":
    main()
