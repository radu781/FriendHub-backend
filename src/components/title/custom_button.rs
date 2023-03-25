use yew::prelude::*;

#[derive(Properties, PartialEq)]
pub struct Props {
    pub label: String,
    pub on_click: Callback<()>,
}

#[function_component(CustomButton)]
pub fn custom_button(props: &Props) -> Html {
    let on_click_copy = props.on_click.clone();
    let button_onclick = Callback::from(move |_| {
        on_click_copy.emit(());
    });
    html! {
        <button onclick={button_onclick}>{&props.label}</button>
    }
}
