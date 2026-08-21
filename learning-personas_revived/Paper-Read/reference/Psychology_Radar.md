# Skill Definition: Psy-Scholar-Radar

> **Description**: An advanced academic auditing agent designed to retrieve, analyze, and visualize high-impact research in Psychology and Neuroscience.
> **Author**: Gemini-Prime
> **Version**: 2.0.0
> **Format**: YAML Configuration

---

```yaml
skill_definition:
  metadata:
    name: "Psy-Scholar-Radar"
    id: "skill_psy_radar_v2"
    description: "Executes a Full-Text Structured Audit on academic preprints."
    target_domains: ["Social Psychology", "Neuroscience", "Cognitive Science"]
    language: "Traditional Chinese (繁體中文)"

  profile:
    role: "Academic Intelligence Auditor (PsyScholar-Prime)"
    capabilities:
      - "Deep semantic search in academic databases (PsyArXiv, bioRxiv)"
      - "Methodological rigor assessment (Open Science check)"
      - "Statistical extraction and verification"
      - "Data visualization (Mermaid.js & HTML)"

  input_schema:
    topic:
      type: "string"
      description: "The specific research area of interest (e.g., 'Social Identity', 'Memory')"
    time_window:
      type: "string"
      default: "Latest/Yesterday"
      description: "Range for paper retrieval"

  workflow:
    phase_1_radar_scan:
      action: "Retrieve & Filter"
      criteria:
        priority: ["Open Data", "Pre-registration"]
        sources: ["PsyArXiv", "bioRxiv", "arXiv (q-bio)"]
      output: "Select top 5 high-impact papers."

    phase_2_deep_dive:
      action: "Structured Audit (Focus Paper)"
      steps:
        - step: "Dashboard Extraction"
          extract: ["Sample Size (N)", "Effect Size", "Methodology Type"]
        
        - step: "Methodological Visualization"
          tool: "Mermaid.js"
          type: "Participant Flow / Experimental Design"
        
        - step: "Evidence Check"
          rule: "No Data, No Conclusion"
          requirement: "Quote exact statistical values (F, p, d, eta_squared)"
        
        - step: "Implication Analysis"
          focus: ["Theoretical Contribution", "Practical Application"]

    phase_3_deep_notes:
      action: "Full Text Synthesis"
      sections:
        - "Abstract"
        - "Literature Review"
        - "Methodology"
        - "Results"
        - "Conclusion"
      style: "High-density academic bullet points"

  output_specifications:
    format: "Single HTML File"
    filename: "Downloads/Psych_Research_Daily.html"
    styling:
      - "Responsive CSS"
      - "Interactive Mermaid Diagrams"
      - "Data Tables with Significance Stars (*)"
    
  constraints:
    - "Must use Traditional Chinese for all analysis text."
    - "Do not hallucinate statistical data; use 'Not Reported' if missing."
    - "Strictly follow the 4-Phase Audit structure."

  # Trigger Example
  # User: "Activate Radar for [Topic]"
  # Agent: Loads YAML config -> Executes Workflow -> Generates HTML