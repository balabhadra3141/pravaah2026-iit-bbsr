def detect_causal_patterns(transcript):
    causes = []

    turns = transcript["conversation"]

    for i, turn in enumerate(turns):

        text = turn["text"].lower()

        # pattern 1: repeated complaint
        if "already called" in text or "again" in text:
            causes.append({
                "type": "Repeated unresolved issue",
                "evidence": turn["text"],
                "turn_index": i
            })

        # pattern 2: escalation request
        if "supervisor" in text:
            causes.append({
                "type": "Explicit escalation request",
                "evidence": turn["text"],
                "turn_index": i
            })

    return causes
