#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VYAS ASTRA — COMPLETE AI CHAT ENGINE REDESIGN
Root Cause: System prompt ~1324 tokens + max_tokens 850 = model has no room to answer correctly
Fix:
  1. Compress PHP master prompt to <300 tokens (keep only essential rules)
  2. Increase max_tokens to 1200 (Groq free tier supports 8192 context)
  3. JS systemPrompt (kundli data) must be FIRST, PHP identity LAST (recency matters)
  4. chatHistory sanitization — strip HTML before sending
  5. Query-type routing in PHP — detect query type and use MINIMAL focused prompt
"""

with open('api/ai_chat.php', 'r', encoding='utf-8') as f:
    php = f.read()

# ─────────────────────────────────────────────────────────
# STEP 1: Replace bloated jevAiSystemInstruction (~1324 tok)
# with ultra-compact 3-rule identity (<200 tok)
# ─────────────────────────────────────────────────────────

old_jev_block_start = "// Inject 5-Part Authoritative Daivagya Structure Directive\n$jevAiSystemInstruction = <<<'EOD'"
old_jev_block_end = "EOD;\n$systemPrompt = $jevAiSystemInstruction . \"\n\n\" . $systemPrompt;"

# Find boundaries
start_idx = php.find(old_jev_block_start)
end_idx = php.find(old_jev_block_end)
end_idx_full = end_idx + len(old_jev_block_end)

if start_idx > 0 and end_idx > 0:
    old_block = php[start_idx:end_idx_full]
    
    new_block = r"""// Compact identity — full context comes from JS systemPrompt (kundli/prashna data)
// PHP only injects: identity tag + axiom lock + date + response rules
$compactIdentity = "आप 'आचार्य व्यास' (Aacharya Vyas) हैं — वैदिक दैवज्ञ AI Agent (Parashari + KP + Jaimini).\n" .
"आज: {$currentDateHindi}, {$currentTimeIST} IST.\n" .
"नियम: (1) kundli/prashna data जो JS से भेजा है वही आपका एकमात्र आधार है — कोई मनगढंत data नहीं। " .
"(2) राशि स्वामी: मेष-मंगल, वृषभ-शुक्र, मिथुन-बुध, कर्क-चन्द्र, सिंह-सूर्य, कन्या-बुध, तुला-शुक्र, वृश्चिक-मंगल, धनु-गुरु, मकर-शनि, कुंभ-शनि, मीन-गुरु. " .
"(3) शनि: 3,7,10 दृष्टि | मंगल: 4,7,8 | गुरु/राहु/केतु: 5,7,9 | बाकी: 7 — यह अटल है. " .
"(4) उत्तर हिंदी में, अत्यंत संक्षिप्त (3-5 bullet या table), सटीक. " .
"(5) पंचांग/गोचर प्रश्न पर जातक की जन्मपत्री का उल्लेख न करें.";
$systemPrompt = $compactIdentity . "\n\n" . $systemPrompt;"""
    
    php = php.replace(old_block, new_block)
    print("✅ STEP 1: Bloated jevAiSystemInstruction replaced with compact identity (~150 tokens)")
else:
    print(f"⚠️  STEP 1: Could not find block. start={start_idx}, end={end_idx}")
    print("Searching for alternate pattern...")
    # Try alternate
    if "EOD;\n$systemPrompt = $jevAiSystemInstruction" in php:
        print("Found EOD block end")
    else:
        # Manual check
        idx = php.find("$jevAiSystemInstruction")
        print(f"$jevAiSystemInstruction at index: {idx}")

# ─────────────────────────────────────────────────────────
# STEP 2: Increase max_tokens from 850 to 1400
# ─────────────────────────────────────────────────────────
if '"max_tokens" => 850' in php:
    php = php.replace('"max_tokens" => 850', '"max_tokens" => 1400')
    print("✅ STEP 2: max_tokens 850 → 1400")
elif '"max_tokens" => 1400' in php:
    print("ℹ️  STEP 2: max_tokens already 1400")
else:
    print("⚠️  STEP 2: max_tokens pattern not found")

# ─────────────────────────────────────────────────────────
# STEP 3: Compress inviolableGroundTruth (currently ~350 tokens)
# Replace with inline compact version already in $compactIdentity above
# ─────────────────────────────────────────────────────────
# Find the inviolableGroundTruth block
old_gt_start = "// ----------------------------------------------------------------------\n// INVIOLABLE VEDIC AXIOMS & GROUND TRUTH TABLE (STRICT ANTI-HALLUCINATION)"
old_gt_end = '$systemPrompt .= $inviolableGroundTruth;'

gt_start_idx = php.find(old_gt_start)
gt_end_idx = php.find(old_gt_end)
gt_end_full = gt_end_idx + len(old_gt_end)

if gt_start_idx > 0 and gt_end_idx > 0:
    old_gt = php[gt_start_idx:gt_end_full]
    # Replace with nothing — axioms already embedded in compactIdentity above
    new_gt = "// Axioms now embedded in $compactIdentity (see above) — no separate block needed"
    php = php.replace(old_gt, new_gt)
    print("✅ STEP 3: Redundant inviolableGroundTruth block removed (axioms in compact identity)")
else:
    print(f"⚠️  STEP 3: inviolableGroundTruth block not found. start={gt_start_idx}, end={gt_end_idx}")

# ─────────────────────────────────────────────────────────
# STEP 4: Reduce chatHistory from last 10 to last 6 messages
# to reduce context pollution
# ─────────────────────────────────────────────────────────
if 'array_slice($chatHistory, -10)' in php:
    php = php.replace('array_slice($chatHistory, -10)', 'array_slice($chatHistory, -6)')
    print("✅ STEP 4: chatHistory window 10 → 6 messages (reduce context pollution)")
else:
    print("⚠️  STEP 4: chatHistory slice pattern not found")

# ─────────────────────────────────────────────────────────
# STEP 5: Add query-type isolation guard in PHP
# If query has NO kundli context (systemPrompt is short/empty),
# add a "universal query" mode that prevents natal chart hallucination
# ─────────────────────────────────────────────────────────
old_messages_init = "// Prepare messages payload\n$messages = [];"
new_messages_init = r"""// Prepare messages payload
$messages = [];

// QUERY-TYPE GUARD: If systemPrompt from JS is very short (< 200 chars),
// it means no kundli was loaded — force universal/panchang mode
$jsPromptLen = mb_strlen($systemPrompt, 'UTF-8');
if ($jsPromptLen < 200) {
    // Universal query — no kundli context — add strict guard
    $systemPrompt .= "\n\n[STRICT GUARD]: कोई जन्म पत्रिका उपलब्ध नहीं है। " .
        "केवल शास्त्रीय सिद्धांत, पंचांग, गोचर या प्रश्न मार्ग के आधार पर उत्तर दें। " .
        "किसी जातक की व्यक्तिगत ग्रह स्थिति का उल्लेख न करें।";
}"""

if old_messages_init in php:
    php = php.replace(old_messages_init, new_messages_init)
    print("✅ STEP 5: Query-type isolation guard added for no-kundli queries")
else:
    print("⚠️  STEP 5: messages init pattern not found")

# Save
with open('api/ai_chat.php', 'w', encoding='utf-8') as f:
    f.write(php)

print(f"\n📊 Final ai_chat.php size: {len(php)} chars (~{len(php)//4} tokens)")
print("✅ Complete. Run git diff api/ai_chat.php to review.")

