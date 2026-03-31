#!/bin/bash
# Template: Code injection methods for CMOJ submit page
# Handles various editor types (textarea, CodeMirror, ACE)

# ============================================================
# Method 1: Simple textarea fill (try first)
# ============================================================
inject_textarea() {
    local ref="$1"
    local code_file="$2"
    # Read code from file and fill
    agent-browser fill "$ref" "$(cat "$code_file")"
}

# ============================================================
# Method 2: CodeMirror injection via eval
# ============================================================
inject_codemirror() {
    local code_file="$1"
    local code_b64=$(base64 < "$code_file")
    
    agent-browser eval --stdin <<EVALEOF
(function() {
    const code = atob('$code_b64');
    
    // Try CodeMirror
    const cm = document.querySelector('.CodeMirror');
    if (cm && cm.CodeMirror) {
        cm.CodeMirror.setValue(code);
        return 'SUCCESS: CodeMirror editor filled';
    }
    
    return 'FAIL: No CodeMirror found';
})()
EVALEOF
}

# ============================================================
# Method 3: ACE Editor injection via eval
# ============================================================
inject_ace() {
    local code_file="$1"
    local code_b64=$(base64 < "$code_file")
    
    agent-browser eval --stdin <<EVALEOF
(function() {
    const code = atob('$code_b64');
    
    // Try ACE
    const aceEl = document.querySelector('.ace_editor');
    if (aceEl && aceEl.env && aceEl.env.editor) {
        aceEl.env.editor.setValue(code, -1);
        return 'SUCCESS: ACE editor filled';
    }
    
    // Try global ace
    if (typeof ace !== 'undefined') {
        const editors = document.querySelectorAll('.ace_editor');
        if (editors.length > 0) {
            const editor = ace.edit(editors[0]);
            editor.setValue(code, -1);
            return 'SUCCESS: ACE editor filled (global)';
        }
    }
    
    return 'FAIL: No ACE editor found';
})()
EVALEOF
}

# ============================================================
# Method 4: Universal fallback (tries all methods)
# ============================================================
inject_universal() {
    local code_file="$1"
    local code_b64=$(base64 < "$code_file")
    
    agent-browser eval --stdin <<EVALEOF
(function() {
    const code = atob('$code_b64');
    
    // Method A: CodeMirror
    const cm = document.querySelector('.CodeMirror');
    if (cm && cm.CodeMirror) {
        cm.CodeMirror.setValue(code);
        return 'SUCCESS via CodeMirror';
    }
    
    // Method B: ACE Editor
    const aceEl = document.querySelector('.ace_editor');
    if (aceEl && aceEl.env && aceEl.env.editor) {
        aceEl.env.editor.setValue(code, -1);
        return 'SUCCESS via ACE';
    }
    
    // Method C: Monaco Editor (VS Code style)
    const monacoEl = document.querySelector('.monaco-editor');
    if (monacoEl && window.monaco) {
        const models = window.monaco.editor.getModels();
        if (models.length > 0) {
            models[0].setValue(code);
            return 'SUCCESS via Monaco';
        }
    }
    
    // Method D: Textarea with name="source" or id="id_source"
    const ta = document.querySelector('#id_source, textarea[name="source"], textarea.submit-code');
    if (ta) {
        // For React/Angular controlled inputs
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLTextAreaElement.prototype, 'value'
        ).set;
        nativeInputValueSetter.call(ta, code);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        return 'SUCCESS via textarea';
    }
    
    // Method E: Any textarea on the page
    const anyTa = document.querySelector('textarea');
    if (anyTa) {
        anyTa.value = code;
        anyTa.dispatchEvent(new Event('input', { bubbles: true }));
        anyTa.dispatchEvent(new Event('change', { bubbles: true }));
        return 'SUCCESS via first textarea';
    }
    
    return 'FAIL: No editor found. Elements on page: ' + 
           Array.from(document.querySelectorAll('textarea, .CodeMirror, .ace_editor, .monaco-editor'))
               .map(el => el.tagName + '.' + el.className).join(', ');
})()
EVALEOF
}

echo "=== Code Injection Templates ==="
echo "Use inject_universal for most cases"
echo "Specify code file as first argument"
