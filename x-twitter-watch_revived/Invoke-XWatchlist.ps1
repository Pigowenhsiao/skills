param(
    [string]$Account = "xiaoxiaodong01",
    [string]$VaultRoot,
    [string[]]$CandidateStatusIds = @(),
    [int]$MaxCandidates = 25,
    [switch]$UpdateState,
    [switch]$WriteReport
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($VaultRoot)) {
    $VaultRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}

$twitterDir = Join-Path $VaultRoot "08-Learning\90_Source-Inbox\twitter"
$watchDir = Join-Path $twitterDir "watchlists"
$rawDir = Join-Path $twitterDir "raw"
New-Item -ItemType Directory -Force -Path $watchDir, $rawDir | Out-Null

$statePath = Join-Path $watchDir "$Account-state.json"
$configPath = Join-Path $watchDir "$Account-watchlist.json"
$runStamp = Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz"
$runDate = Get-Date -Format "yyyy-MM-dd"

function Convert-MojibakeUtf8 {
    param([AllowNull()][string]$Text)
    if ($null -eq $Text) { return "" }
    try {
        return [Text.Encoding]::UTF8.GetString([Text.Encoding]::GetEncoding(28591).GetBytes($Text))
    } catch {
        return $Text
    }
}

function Get-IdsFromFiles {
    param([string]$Root, [string]$Account)
    $ids = New-Object System.Collections.Generic.HashSet[string]
    $targets = @(
        (Join-Path $Root "00-Inbox"),
        (Join-Path $Root "08-Learning\90_Source-Inbox\twitter"),
        (Join-Path $Root "03-Resources\003-Visual-Design-Presentation-Workflows"),
        (Join-Path $Root "09-Article-Notes")
    ) | Where-Object { Test-Path $_ }

    foreach ($dir in $targets) {
        Get-ChildItem -LiteralPath $dir -Recurse -File -Include *.md,*.json -ErrorAction SilentlyContinue | ForEach-Object {
            $content = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
            if ([string]::IsNullOrWhiteSpace($content)) { return }
            foreach ($m in [regex]::Matches($content, "$Account/status/([0-9]{10,})")) { [void]$ids.Add($m.Groups[1].Value) }
            foreach ($m in [regex]::Matches($content, '"tweet_id"\s*:\s*"([0-9]{10,})"')) { [void]$ids.Add($m.Groups[1].Value) }
            foreach ($m in [regex]::Matches($content, 'source_id:\s*"([0-9]{10,})"')) { [void]$ids.Add($m.Groups[1].Value) }
        }
    }
    return @($ids)
}

function Get-DuckDuckGoCandidateIds {
    param([string]$Account)
    $ids = New-Object System.Collections.Generic.HashSet[string]
    $queries = @(
        "site:x.com/$Account/status $Account",
        "site:x.com/$Account/status x.com/i/article $Account",
        "site:twitter.com/$Account/status $Account GPT2",
        "site:x.com/$Account/status $Account GPT2 PPT prompt"
    )
    foreach ($query in $queries) {
        $url = "https://duckduckgo.com/html/?q=$([uri]::EscapeDataString($query))"
        try {
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 25 -Headers @{ "User-Agent" = "Mozilla/5.0" }
            foreach ($m in [regex]::Matches($response.Content, "$Account/status/([0-9]{10,})")) { [void]$ids.Add($m.Groups[1].Value) }
        } catch {
            Write-Warning "DuckDuckGo discovery failed for query '$query': $($_.Exception.Message)"
        }
    }
    return @($ids)
}

function Get-TwStalkerCandidateIds {
    param([string]$Account)
    $ids = New-Object System.Collections.Generic.HashSet[string]
    $urls = @(
        "https://twstalker.com/$Account",
        "https://w.twstalker.com/$Account",
        "https://www6.twstalker.com/$Account"
    )
    foreach ($url in $urls) {
        try {
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 20 -Headers @{ "User-Agent" = "Mozilla/5.0" }
            foreach ($m in [regex]::Matches($response.Content, "$Account/status/([0-9]{10,})")) { [void]$ids.Add($m.Groups[1].Value) }
        } catch {
            Write-Warning "TwStalker discovery failed for '$url': $($_.Exception.Message)"
        }
    }
    return @($ids)
}

function Get-FxStatus {
    param([string]$Account, [string]$StatusId)
    $fxUrl = "https://api.fxtwitter.com/$Account/status/$StatusId"
    $vxUrl = "https://api.vxtwitter.com/$Account/status/$StatusId"
    $result = [ordered]@{
        status_id = $StatusId
        status_url = "https://x.com/$Account/status/$StatusId"
        fetched_at = $runStamp
        fetched_via = $null
        ok = $false
        error = $null
        created_at = $null
        text = $null
        article_id = $null
        article_url = $null
        title = $null
        preview_text = $null
        likes = $null
        reposts = $null
        replies = $null
        bookmarks = $null
        views = $null
    }

    try {
        $json = Invoke-RestMethod -Uri $fxUrl -Method Get -TimeoutSec 25
        if ($json.code -eq 200 -and $json.tweet) {
            $tweet = $json.tweet
            $result.ok = $true
            $result.fetched_via = "fxtwitter"
            $result.created_at = $tweet.created_at
            $result.text = Convert-MojibakeUtf8 $tweet.text
            $result.likes = $tweet.likes
            $result.reposts = if ($null -ne $tweet.retweets) { $tweet.retweets } else { $tweet.reposts }
            $result.replies = $tweet.replies
            $result.bookmarks = $tweet.bookmarks
            $result.views = $tweet.views
            if ($tweet.article) {
                $result.article_id = $tweet.article.id
                $result.article_url = "https://x.com/i/article/$($tweet.article.id)"
                $result.title = Convert-MojibakeUtf8 $tweet.article.title
                $result.preview_text = Convert-MojibakeUtf8 $tweet.article.preview_text
            }
            return [pscustomobject]$result
        }
    } catch {
        $result.error = "fxtwitter: $($_.Exception.Message)"
    }

    try {
        $json = Invoke-RestMethod -Uri $vxUrl -Method Get -TimeoutSec 25
        $result.ok = $true
        $result.fetched_via = "vxtwitter"
        $result.created_at = $json.date
        $result.text = $json.text
        $result.likes = $json.likes
        $result.reposts = $json.retweets
        $result.replies = $json.replies
        if ($json.article) {
            $result.article_id = if ($json.text -match '/article/([0-9]{10,})') { $Matches[1] } else { $null }
            $result.article_url = if ($result.article_id) { "https://x.com/i/article/$($result.article_id)" } else { $json.text }
            $result.title = $json.article.title
            $result.preview_text = $json.article.preview_text
        }
    } catch {
        if ($result.error) { $result.error += "; vxtwitter: $($_.Exception.Message)" } else { $result.error = "vxtwitter: $($_.Exception.Message)" }
    }
    return [pscustomobject]$result
}

$knownFromVault = Get-IdsFromFiles -Root $VaultRoot -Account $Account
$state = [ordered]@{
    account = $Account
    created_at = $runStamp
    updated_at = $runStamp
    known_status_ids = @($knownFromVault | Sort-Object -Unique)
    last_run = $null
}

if (Test-Path $statePath) {
    try {
        $loaded = Get-Content -LiteralPath $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
        $known = @($loaded.known_status_ids) + $knownFromVault | Where-Object { $_ } | Sort-Object -Unique
        $state.created_at = if ($loaded.created_at) { $loaded.created_at } else { $runStamp }
        $state.known_status_ids = @($known)
    } catch {
        Write-Warning "Failed to read state file; recreating from Vault scan: $($_.Exception.Message)"
    }
}

$candidateIds = New-Object System.Collections.Generic.HashSet[string]
foreach ($id in $CandidateStatusIds) { if ($id -match '^[0-9]{10,}$') { [void]$candidateIds.Add($id) } }
foreach ($id in (Get-DuckDuckGoCandidateIds -Account $Account)) { [void]$candidateIds.Add($id) }
foreach ($id in (Get-TwStalkerCandidateIds -Account $Account)) { [void]$candidateIds.Add($id) }

$allCandidates = @($candidateIds) | Sort-Object -Descending | Select-Object -First $MaxCandidates
$knownSet = New-Object System.Collections.Generic.HashSet[string]
foreach ($id in $state.known_status_ids) { [void]$knownSet.Add([string]$id) }
$newIds = @($allCandidates | Where-Object { -not $knownSet.Contains([string]$_) })

$items = @()
foreach ($id in $newIds) { $items += Get-FxStatus -Account $Account -StatusId $id }

$run = [ordered]@{
    account = $Account
    run_at = $runStamp
    candidates_checked = @($allCandidates)
    known_count_before = @($state.known_status_ids).Count
    new_status_ids = @($newIds)
    items = @($items)
    discovery_notes = @(
        "Primary discovery uses DuckDuckGo HTML search and public TwStalker mirrors.",
        "Full status/article enrichment uses fxtwitter first and vxtwitter fallback.",
        "If public discovery returns no latest IDs, pass -CandidateStatusIds manually with copied X status IDs."
    )
}

$rawPath = Join-Path $rawDir "$runDate`_$Account-watch-run.json"
$run | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath $rawPath -Encoding UTF8

if ($UpdateState) {
    $updatedKnown = @($state.known_status_ids) + @($items | Where-Object { $_.ok } | ForEach-Object { $_.status_id }) | Sort-Object -Unique
    $state.updated_at = $runStamp
    $state.known_status_ids = @($updatedKnown)
    $state.last_run = $run
    $state | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath $statePath -Encoding UTF8
}

if ($WriteReport) {
    $reportPath = Join-Path $watchDir "$Account-watchlist.md"
    $newLines = if ($items.Count -gt 0) {
        ($items | ForEach-Object {
            $title = if ($_.title) { $_.title } elseif ($_.text) { $_.text } else { "未取得標題" }
            "- [$($_.status_id)]($($_.status_url)) - $title / fetched_via=$($_.fetched_via) / ok=$($_.ok)"
        }) -join "`n"
    } else {
        "- 本次沒有找到新的未收 status ID。"
    }
    $report = @"
---
title: "@${Account} X Watchlist"
source: "X / public mirrors"
source_account: "$Account"
updated: "$runDate"
type: "watchlist"
status: "active"
tags:
  - llm-wiki
  - x-watchlist
  - xiaoxiaodong01
---

# @$Account X Watchlist

## 用途

追蹤 @$Account 的新貼文候選 ID。這個 watcher 只負責發現與 raw capture，不自動產生正式長文筆記；發現值得整理的新貼文後，再用 `llm-wiki summary <url> save in Vault and Notion` 處理。

## 本次執行

- Run at: $runStamp
- Candidates checked: $($allCandidates.Count)
- Known before: $($run.known_count_before)
- New IDs: $($newIds.Count)
- Raw run: 08-Learning/90_Source-Inbox/twitter/raw/$runDate`_$Account-watch-run.json
- State: 08-Learning/90_Source-Inbox/twitter/watchlists/$Account-state.json

## 新候選

$newLines

## 執行指令

~~~powershell
& "14-Skills\x-twitter-watch\Invoke-XWatchlist.ps1" -Account "$Account" -UpdateState -WriteReport
~~~

如果公開 discovery 沒抓到最新貼文，但你手上有 status URL，可用：

~~~powershell
& "14-Skills\x-twitter-watch\Invoke-XWatchlist.ps1" -Account "$Account" -CandidateStatusIds "2056412276593410537" -UpdateState -WriteReport
~~~

## 限制

- Public mirror / search engine 可能延遲、限流或漏貼文。
- TwStalker 目前常回 403；DuckDuckGo 可能只找到已索引舊貼文。
- Notion 同步仍依賴有效 `NOTION_TOKEN`；目前已知會回 `401 Unauthorized`。
"@
    Set-Content -LiteralPath $reportPath -Value $report -Encoding UTF8
}

[pscustomobject]$run | ConvertTo-Json -Depth 30


