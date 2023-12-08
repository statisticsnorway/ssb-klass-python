from datetime import date

import ipywidgets as widgets
from IPython.display import HTML
from IPython.display import display

from klass.classes.search import KlassSearchClassifications
from klass.requests.sections import sections_dict


def search_classification(no_dupes: bool = True) -> widgets.VBox:
    """Open a GUI in Jupyter Notebooks using ipywidgets.

    Lets you search for terms and copy sample code out,
    that'll let you get data from the classification.

    Args:
        no_dupes (bool): To include duplicate results or not in the result.
                        Dupes are caused by multiple languages being returned.

    Returns:
        widgets.VBox: Containing the nested ipywidgets-GUI. Jupyter will automatically display it.
    """
    search_result: widgets.output = widgets.Output()
    search_term: widgets.Text = widgets.Text(
        value="", placeholder="Searchterm", description="Type searchterm:"
    )
    section_dropdown: widgets.Dropdown = widgets.Dropdown(
        options=["Choose..."], value="Choose...", description="Section:", disabled=False
    )

    def do_search(btn: widgets.Button) -> None:
        nonlocal search_term
        nonlocal section_dropdown
        nonlocal search_result

        with search_result:
            search_result.clear_output()
            display("Searching...")  # type: ignore
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
                    var_name = "_".join(
                        cl["name"]
                        .split(":")[0]
                        .lower()
                        .replace("æ", "ae")
                        .replace("ø", "oe")
                        .replace("å", "aa")
                        .strip()
                    )
                    var_name_chars = [c if c.isalnum() else "_" for c in var_name]
                    var_name_true = "".join(
                        [c for c in var_name_chars if c and c != " "]
                    )
                    if len(var_name_true.split("_")) > 3:
                        var_name_true = "_".join(
                            [part for part in var_name_true.split("_")[:3] if part]
                        )
                    text = f"""from klass import KlassClassification\\n{var_name_true} = KlassClassification({cl["classification_id"]})\\n{var_name_true}.get_codes(\\'{date.today().strftime('%Y-%m-%d')}\\').data"""
                    # var_name = "klass" + str(cl["classification_id"])
                    search_content += f"""<button class="classification_copy_code" onclick="navigator.clipboard.writeText('{text}')">Copy code</button> {cl["classification_id"]} - {cl["name"]}<br />"""
            else:
                search_content = "Found no matching classifications."
        except Exception as e:
            search_content = str(e)

        with search_result:
            search_result.clear_output()
            display(HTML(search_content))  # type: ignore

    sections = ["Choose...", *list(sections_dict().keys())]
    section_dropdown = widgets.Dropdown(
        options=sections, value=sections[0], description="Section:", disabled=False
    )
    search_button = widgets.Button(description="Search")
    search_button.on_click(do_search)
    html_header = widgets.HTML(
        value="<style>button.classification_copy_code:active {opacity: 30%;} button.classification_copy_code:hover {opacity: 80%;}</style>"
    )

    return widgets.VBox(
        [
            widgets.HBox([html_header, search_term, section_dropdown, search_button]),
            widgets.HBox([search_result]),
        ]
    )
