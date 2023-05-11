import ipywidgets as widgets
from IPython.display import display, clear_output, HTML
from klass import KlassSearchClassifications, KlassSearchFamilies, sections_dict

def search_classification():
    def do_search(btn):
        nonlocal search_term
        nonlocal section_dropdown
        nonlocal search_result
        
        if not search_term.value:
            search_term_value = "1"
        else:
            search_term_value = search_term.value
        
        if section_dropdown.value != "Choose...":
            search_class = KlassSearchClassifications(search_term_value, ssbsection=section_dropdown.value)
        else:
            search_class = KlassSearchClassifications(search_term_value)
        search_content = ""
        for cl in search_class.classifications:
            var_name = (cl["name"]
                        .split(":")[0]
                        .lower()
                        .replace(" ", "_")
                        .replace("(", "")
                        .replace(")", "")
                        .replace("æ", "ae")
                        .replace("ø", "oe")
                        .replace("å", "aa")
                        .strip())
            text = f'''from klass import KlassClassification\\n{var_name} = KlassClassification({cl["classification_id"]})\\n{var_name}.get_codes().data'''
            var_name = "klass" + str(cl["classification_id"])
            script_var = f"<script>var {var_name} = '{text}'</script>"
            search_content += f'''<button onclick="navigator.clipboard.writeText('{text}')">Copy code</button> {cl["classification_id"]} - {cl["name"]}<br />'''


        
        with search_result:
            search_result.clear_output()
            display(HTML(search_content))
    
    
    search_term = widgets.Text(value="",
                              placeholder="Searchterm",
                              description="Type searchterm:")
    sections = ["Choose..."] + list(sections_dict().keys())
    section_dropdown = widgets.Dropdown(options=sections,
                                            value=sections[0],
                                            description="Section:",
                                            disabled=False)
    search_button = widgets.Button(description="Search")
    search_button.on_click(do_search)
    
    search_result = widgets.Output()
    #display(search_result)
    
    return widgets.VBox([
        widgets.HBox([search_term, section_dropdown, search_button]),
        widgets.HBox([search_result])
    ])


