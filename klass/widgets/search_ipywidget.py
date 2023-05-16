import ipywidgets as widgets
from IPython.display import HTML, display

from klass import KlassSearchClassifications, sections_dict


def search_classification(no_dupes=True):
    def do_search(btn):
        nonlocal search_term
        nonlocal section_dropdown
        nonlocal search_result

        with search_result:
            search_result.clear_output()
            display("Searching...")
            # Add loading-gif?

        try:
            if section_dropdown.value != "Choose...":
                search_class = KlassSearchClassifications(
                    search_term.value,
                    ssbsection=section_dropdown.value,
                    include_codelists=True,
                    no_dupes=no_dupes,
                )
            else:
                search_class = KlassSearchClassifications(
                    search_term.value, include_codelists=True, no_dupes=no_dupes
                )
            search_content = ""
            print(f"{search_class.classifications=}")
            if len(search_class.classifications):
                for cl in search_class.classifications:
                    var_name = (
                        cl["name"]
                        .split(":")[0]
                        .lower()
                        .replace(" ", "_")
                        .replace("(", "")
                        .replace(")", "")
                        .replace("æ", "ae")
                        .replace("ø", "oe")
                        .replace("å", "aa")
                        .strip()
                    )
                    text = f"""from klass import KlassClassification\\n{var_name} = KlassClassification({cl["classification_id"]})\\n{var_name}.get_codes().data"""
                    var_name = "klass" + str(cl["classification_id"])
                    search_content += f"""<button onclick="navigator.clipboard.writeText('{text}')">Copy code</button> {cl["classification_id"]} - {cl["name"]}<br />"""
            else:
                search_content = "Found no matching classifications."
        except Exception as e:
            search_content = str(e)

        with search_result:
            search_result.clear_output()
            display(HTML(search_content))

    search_term = widgets.Text(
        value="", placeholder="Searchterm", description="Type searchterm:"
    )
    sections = ["Choose..."] + list(sections_dict().keys())
    section_dropdown = widgets.Dropdown(
        options=sections, value=sections[0], description="Section:", disabled=False
    )
    search_button = widgets.Button(description="Search")
    search_button.on_click(do_search)

    search_result = widgets.Output()

    return widgets.VBox(
        [
            widgets.HBox([search_term, section_dropdown, search_button]),
            widgets.HBox([search_result]),
        ]
    )
