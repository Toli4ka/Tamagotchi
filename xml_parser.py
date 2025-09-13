try:
    import ure as re
except ImportError:
    import re

# XML attribute parser
_attr_re = r'([\w:-]+)\s*=\s*"([^"]*)"'

def _parse_attrs(tag_text):
    attrs = {}
    for m in re.finditer(_attr_re, tag_text):
        attrs[m.group(1)] = m.group(2)
    return attrs

def _extract_sections(xml_text, tag_name):
    # Extracts <tag_name ...> ... </tag_name> blocks and returns [(attrs, inner_xml), ...]
    sections = []
    start_pat = "<" + tag_name
    end_pat = "</" + tag_name + ">"
    i = 0
    while True:
        i = xml_text.find(start_pat, i)
        if i == -1:
            break
        j = xml_text.find(">", i)
        if j == -1:
            break
        tag_start = xml_text[i:j+1]
        attrs = _parse_attrs(tag_start)
        k = xml_text.find(end_pat, j+1)
        if k == -1:
            inner = ""
            i = j + 1
        else:
            inner = xml_text[j+1:k]
            i = k + len(end_pat)
        sections.append((attrs, inner))
    return sections

def _extract_first_tag_text(xml_text, tag):
    open_tag = "<{}>".format(tag)
    close_tag = "</{}>".format(tag)
    i = xml_text.find(open_tag)
    if i == -1:
        return None
    j = xml_text.find(close_tag, i + len(open_tag))
    if j == -1:
        return None
    return xml_text[i + len(open_tag):j]

def _parse_departures(xml_text):
    """ 
    Parses departures;
    returns a list of dicts:
        { "stop_id": str,
          "departure": {line_number, planned_time, planned_platform, planned_path} or None
        }
    """
    departures = []
    for s_attrs, s_inner in _extract_sections(xml_text, "s"):
        # Look for a self-closing <dp .../> inside the <s> block
        m = re.search(r"<dp\s+[^>]*/>", s_inner)
        departure = None
        if m:
            dp_attrs = _parse_attrs(m.group(0))
            departure = {
                "line_number": dp_attrs.get("l"),
                "planned_time": dp_attrs.get("pt"),
                "planned_platform": dp_attrs.get("pp"),
                "planned_path": dp_attrs.get("ppth"),
            }
        departures.append({"stop_id": s_attrs.get("id"), "departure": departure})
    return departures

def _parse_changes(xml_text):
    """
    Parse timetable changes; 
    returns a list of dicts:   
        { "stop_id": str,
          "dp_changes": {changed_time, changed_platform, cancelled, other_changes}
        }
    """
    changes = []
    for s_attrs, s_inner in _extract_sections(xml_text, "s"):
        stop_id = s_attrs.get("id")

        m = re.search(r"<dp\b[^>]*/?>", s_inner)
        dp_changes = None
        if m:
            dp_attrs = _parse_attrs(m.group(0))
            dp_changes = {}
         
            if "ct" in dp_attrs:
                dp_changes["changed_time"] = dp_attrs["ct"]
           
            if "cp" in dp_attrs:
                dp_changes["changed_platform"] = dp_attrs["cp"]

            if "clt" in dp_attrs:
                dp_changes["cancelled"] = True

            if ("cde" in dp_attrs) or ("cpth" in dp_attrs) or ("dc" in dp_attrs):
                dp_changes["other_changes"] = True

            if not dp_changes:
                dp_changes = None

        if dp_changes:
            changes.append({"stop_id": stop_id, "dp_changes": dp_changes})
    return changes