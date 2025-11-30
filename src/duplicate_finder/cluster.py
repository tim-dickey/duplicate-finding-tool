from typing import List, Tuple, Dict, Set
from .core import FileSignature

def build_clusters(pairs: List[Tuple[float, FileSignature, FileSignature]]):
    """Convert pair list into cluster dicts.
    Returns list of clusters sorted by representative path.
    Cluster dict: {'representative': str, 'members': [paths], 'size': int, 'max_similarity': float}
    """
    adj: Dict[str, Set[str]] = {}
    max_sim: Dict[str, float] = {}
    for sim, a, b in pairs:
        adj.setdefault(a.path, set()).add(b.path)
        adj.setdefault(b.path, set()).add(a.path)
        max_sim[a.path] = max(max_sim.get(a.path, 0.0), sim)
        max_sim[b.path] = max(max_sim.get(b.path, 0.0), sim)
    visited: Set[str] = set()
    clusters = []
    for node in sorted(adj.keys()):
        if node in visited:
            continue
        stack = [node]
        members: Set[str] = set()
        max_cluster_sim = 0.0
        while stack:
            cur = stack.pop()
            if cur in visited:
                continue
            visited.add(cur)
            members.add(cur)
            max_cluster_sim = max(max_cluster_sim, max_sim.get(cur, 0.0))
            for nxt in adj.get(cur, []):
                if nxt not in visited:
                    stack.append(nxt)
        sorted_members = sorted(members)
        representative = sorted_members[0]
        clusters.append({
            'representative': representative,
            'members': sorted_members,
            'size': len(sorted_members),
            'max_similarity': max_cluster_sim,
        })
    clusters.sort(key=lambda c: (c['representative'], -c['size']))
    return clusters
