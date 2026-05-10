def compare_assessments(results):

    if len(results) < 2:
        return "I could not find enough assessments to compare."

    a = results[0]
    b = results[1]

    comparison = f"""
Comparison between {a['name']} and {b['name']}:

{a['name']}
- Category: {', '.join(a.get('keys', []))}
- Duration: {a.get('duration', 'N/A')}
- Remote Support: {a.get('remote', 'N/A')}
- Adaptive/IRT: {a.get('adaptive', 'N/A')}

{b['name']}
- Category: {', '.join(b.get('keys', []))}
- Duration: {b.get('duration', 'N/A')}
- Remote Support: {b.get('remote', 'N/A')}
- Adaptive/IRT: {b.get('adaptive', 'N/A')}

Summary:
Both assessments evaluate different competencies and can be used together depending on hiring requirements.
"""

    return comparison