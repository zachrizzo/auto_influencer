from image_gen import ImageGenerator
from instagram_bot import InstaBot
import streamlit as st
import os
import asyncio
import time
from threading import Thread

# Set page configuration
st.set_page_config(page_title='Image Generator', layout='wide')


def add_account():
    insta_reference_account = st.session_state['insta_account_input']
    if insta_reference_account and insta_reference_account not in st.session_state['insta_accounts']:
        st.session_state['insta_accounts'].append(insta_reference_account)
        st.success(f'Account {insta_reference_account} added!')
        # Reset the input field
        st.session_state['insta_account_input'] = ''

def remove_account(account_to_remove):
    if account_to_remove in st.session_state['insta_accounts']:
        st.session_state['insta_accounts'].remove(account_to_remove)
        st.experimental_rerun()

def run_async_function(generator, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generator.continuous_img_gen(*args))
    loop.close()

def main():
    st.title('Image Generator')

    # Initialize session state for Instagram accounts list and login status
    if 'insta_accounts' not in st.session_state:
        st.session_state['insta_accounts'] = []
    if 'insta_account_input' not in st.session_state:
        st.session_state['insta_account_input'] = ''
    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False
     # Initialize the insta_bot instance in the session state
    if 'insta_bot' not in st.session_state:
        st.session_state['insta_bot'] = InstaBot()

    # Sidebar for Instagram reference
    with st.sidebar:
        st.header("Instagram Automation")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input('Enter an Instagram account:', key='insta_account_input', on_change=add_account)
            save_img_path = st.text_input('Enter the path to save images:', value='../Fooocus/outputs/refrence_images_from_insta')
        with col2:
            st.button('Add Account', on_click=add_account)

        # Display the list of accounts with remove buttons
        st.write("Accounts to retrieve images from:")
        for account in st.session_state['insta_accounts']:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(account)
            with col2:
                if st.button(f"X", key=account):
                    remove_account(account)

        # Login details for Instagram
        full_screen = st.checkbox('Use Full Screen')
        email = st.text_input('Email')
        password = st.text_input('Password', type='password')



        if st.button('Login to Instagram'):
            if email and password:

                st.session_state['insta_bot'] = InstaBot()
                st.session_state['insta_bot'].open_insta(full_screen)
                st.session_state['is_logged_in'] = st.session_state['insta_bot'].login(email=email, password=password)


        if st.session_state['is_logged_in']:
            if st.button('Get Reference Images from Instagram'):
                if st.session_state['insta_accounts'] and save_img_path:

                    st.session_state['insta_bot'].copy_images(st.session_state['insta_accounts'], save_img_path)
                    st.success('Images retrieved!')
                else:
                    st.error('Please add at least one account and specify a path to save images.')

    # Main page for image generation
    st.header('Generate Your Image')



    prompt = st.text_input("Enter a prompt for image generation:", value="")

    number_of_images_col, performance_col = st.columns([1, 1])

    with performance_col:
        performance = st.radio('Performance', ['Speed', 'Quality', 'Extreme Speed'],horizontal=True ,  index=0)

    with number_of_images_col:
        number_of_images =st.slider('Number of Images', min_value=1, max_value=32, value=1, step=1)


    img_prompt_col, settings_col = st.columns([1, 1])

    with img_prompt_col:
        use_img_prompt = st.checkbox('Use Image Prompt')
        if use_img_prompt:

            model_face_path = st.text_input("Enter the path your model's face photo:", value='/Users/zachrizzo/programing/ai_influencer/Fooocus/outputs/sophoie/face.png')
            if os.path.isfile(model_face_path):
                st.image(model_face_path, caption='Model Face', width=300)
            #slider for weight of model face
            stop_at_col, weight_col = st.columns([1, 1])
            with stop_at_col:
                model_face_stop_at_face = st.slider('Model Face Stop At', min_value=0.0, max_value=1.0, value=0.9, step=0.001)

            with weight_col:
                model_face_weight_face = st.slider('Model Face Weight', min_value=0.0, max_value=2.0, value=0.75, step=0.001)



            img_path = st.text_input('Enter the path to an reference photo dir:', value='/Users/zachrizzo/programing/ai_influencer/Fooocus/outputs/refrence_images_from_insta')

            #slider for weight of image prompt
            stop_at_col, weight_col = st.columns([1, 1])

            with stop_at_col:
                img_prompt_stop_at_img1 = st.slider('Image Prompt Stop At', min_value=0.0, max_value=1.0, value=0.5, step=0.001)

            with weight_col:
                img_prompt_weight_img_1 = st.slider('Image Prompt Weight', min_value=0.0, max_value=2.0, value=0.6, step=0.001)







    with settings_col:
        use_negative_prompt = st.checkbox('Use Negative Prompt')
        if use_negative_prompt:
            negative_prompt = st.text_input('Enter a negative prompt for image generation:')
        else:
            negative_prompt = ''

    continuous_img_gen = st.checkbox('Continuous Image Generation', key='continuous_image_generation', value=True)

    if st.button('Generate Image', key='generate_image'):
        with st.spinner('Generating image...'):
            generator = ImageGenerator()
            if continuous_img_gen:
                # Start a new thread to run the async function
                args = (prompt, negative_prompt, performance, number_of_images, use_img_prompt, model_face_path, model_face_stop_at_face, model_face_weight_face, img_path, img_prompt_stop_at_img1, img_prompt_weight_img_1)
                thread = Thread(target=run_async_function, args=(generator,) + args)
                thread.start()
                thread.join()  # Wait for the async function to complete
                # You might want to handle the results or state updates here
            else:
                image_path = generator.generate_image(prompt, image_path=model_face_path)
                st.success('Image generated!')
                st.image(image_path, caption=prompt)









if __name__ == '__main__':
    main()
