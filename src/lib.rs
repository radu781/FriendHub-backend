use gloo::console::log;
use yew::prelude::*;
mod components;
use components::title::main_title::MainTitle;
use components::bigger::custom_form::CustomForm;

#[function_component(App)]
pub fn app() -> Html {
    let main_title_load = Callback::from(|message: String| log!(message));
    html! {
        <>
        <MainTitle title="123" on_load={main_title_load}/>
        <CustomForm/>
        </>
    }
}
