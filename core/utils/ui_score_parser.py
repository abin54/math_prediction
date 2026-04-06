
import re

class UIScoreParser:
    @staticmethod
    def parse_mi_vs_dc_cricbuzz(tree_text):
        """
        Parses Cricbuzz UI tree for runs/wickets and overs.
        Example tree fragment: 'Mumbai Indians 25/2 (4.0)' or similar.
        """
        # Pattern 1: MI 25/2 (4.0)
        p1 = r"(?i)(MI|Mumbai Indians)\s+(\d+/\d+)\s*\((\d+\.\d+)\)"
        m1 = re.search(p1, tree_text)
        if m1:
            score = m1.group(2)
            overs = float(m1.group(3))
            return score, overs
            
        # Pattern 2: MI 25-2 4.0 overs
        p2 = r"(?i)(MI|Mumbai Indians)\s+(\d+-\d+)\s+(\d+\.\d+)\s+overs"
        m2 = re.search(p2, tree_text)
        if m2:
            score = m2.group(2).replace('-', '/')
            overs = float(m3.group(3))
            return score, overs
            
        # Pattern 3: Simple digit search for fallback
        # This is riskier but helps if the team name is lost in the tree
        p3 = r"(\d+/\d+)\s*\((\d+\.\d+)\)"
        m3 = re.search(p3, tree_text)
        if m3:
            return m3.group(1), float(m3.group(2))
            
        return None, None

    @staticmethod
    def parse_mi_vs_dc_google(tree_text):
        """
        Parses Google Live Score widget.
        Google structure: 'MI 25/2', '4.0 overs' in separate nodes often.
        """
        # Look for the team name first
        if "MI" not in tree_text and "Mumbai" not in tree_text:
            return None, None
            
        score_match = re.search(r"(\d+/\d+)", tree_text)
        over_match = re.search(r"(\d+\.\d+)\s+overs", tree_text)
        
        if score_match and over_match:
            return score_match.group(1), float(over_match.group(1))
            
        return None, None
