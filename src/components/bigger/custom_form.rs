use std::ops::Deref;

use crate::components::title::custom_button::CustomButton;
use crate::components::title::text_input::TextInput;
use gloo::console::log;
use gloo::timers::callback;
use yew::prelude::*;

#[derive(Default)]
struct Data {
    pub username: String,
    pub count: u32,
}

#[function_component(CustomForm)]
pub fn custom_form() -> Html {
    let state = use_state(|| Data::default());
    let cloned_state = state.clone();

    let username_state = use_state(|| "no username set".to_owned());
    let username_changed = Callback::from(move |username: String| {
        cloned_state.set(Data { username, ..*cloned_state.deref().clone() });
    });

    let button_count_state = use_state(|| 0_u32);
    let clones_button_count_state = button_count_state.clone();
    let button_clicked = Callback::from(move |_| {
        let count = *clones_button_count_state;
        clones_button_count_state.set(count + 1);
    });

    html! {
        <div>
        <TextInput name="username" on_change={username_changed}/>
        <CustomButton label="what" on_click={button_clicked}/>
        <p>{"Username: "}{&*username_state}</p>
        <p>{"Button was clicked "}{*button_count_state}{" times"}</p>
        </div>
    }
}
