import streamlit as st 
from PIL import Image
import os
from descriptor import generate_description

# Load image

form_data = []


active_description = ""

def sketch_description(string):
    modification_prompt = fr'''
    Uploaded Sketch Description:

    {string}
    \n
    ----------------------------------------------------------------
    '''

    prompt += string
    print('building prompt complete', prompt)
    return modification_prompt


def user_modification(string):
    modification_prompt = fr'''
    Required Modification to user sketch:

    {string}
    \n
    ---------------------------------------------------------------

    INSTRUCTION:
    Kindly to the best of your ability, modify the sketch to meet the requirements and provide a description of the modification. Example

    ""
    Uploaded Sketch Description:



    ""
    '''

    prompt += string
    print('building prompt complete', prompt)
    return modification_prompt


# open app in wide mode by default
st.set_page_config(layout="wide")   

st.markdown('#### Gen App')
col1, col2 = st.columns(2)

with col1:

    showButton = False

    def build_description_request(option, instruction):
        resp = None
        # add the option to the form data
        form_data.append(option)
        
        # modify the instruction
        _instruction = fr'''
        {instruction}

        Kind Note:
        The Image uploaded is of type {option}
        '''
        form_data.append(_instruction)

        if form_data:
            # st.success("Form data received!")
            try:
                description = generate_description(form_data[0], _instruction)
                
                response = {
                        'description': description, 
                        'status':200
                        }
                resp = response
                return response
            except Exception as e:
                response = {
                    'error':e,
                    'status':404
                }
                resp = response
                return response
                
        return resp


    st.markdown("##### Upload Sketch")
    with st.form(key='my_form'):
        # sketch = st.file_uploader('Upload Sketch', type=['png', 'jpg', 'jpeg'])

        uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

        if uploaded_file is not None:
            st.write('Uploaded Image:')
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Sketch Image", use_column_width=True)

            # Save the image to the 'uploads' folder
            upload_dir = 'uploads'
            os.makedirs(upload_dir, exist_ok=True)
            image_path = os.path.join(upload_dir, uploaded_file.name)
            image.save(image_path)

            # pop a success message.
            st.success("Image Uploaded Successfully!")

            # Get the image path and name
            image_path = os.path.abspath(image_path)
            image_name = os.path.basename(image_path)

            # Add the image path to the form data
            form_data.append(image_path)

            st.write(f"Image path: {repr(image_path)}")
            st.write(f"Image name: {image_name}")


        submit_button = st.form_submit_button(label='Process Sketch')

        if submit_button:
            showButton = True
    

with col2:
    showOldDescription = False

    # Describe Modification.
    st.markdown("##### Generate Image Description")

    with st.form(key='prompt_generation_form'):
        # image type.
        option = st.selectbox('Choose the uploaded image type', ('Sketch', 'Image'))

        # instruction.
        instruction = st.text_input('Basic Instruction', help="Provide a basic instruction for the model to follow. Example: 'Draw a sketch of a dog'")

        submit_button = st.form_submit_button(label='Generate Description')

        if submit_button:
            description = build_description_request(option, instruction)
            if description['status'] != 404:
                active_description = description['description']
                st.markdown("###### Generated Description ")
                st.markdown("``` Model Used: Gemini Pro Vision ```")

                desc = fr'''
                {active_description}

                '''
                st.markdown(desc)
            else:
                st.markdown("###### Experienced A breakdown ")
                desc = fr'''
                *Encountered Error Details*
                {description['error']}

                '''
                st.markdown(desc)

    if active_description != "":
            with st.form(key='modify_response'):
                edit = st.text_input('Suggest Modification to the description')
                submission = st.form_submit_button(label='modify')

                if submission:
                    showOldDescription = True

                    modified = fr'''
                    for this suggested description:
                    {active_description}

                    # Suggested User Modification:
                    {edit}

                    '''
                    modified_description = build_description_request(option, instruction)
                    active_description = modified_description
                    st.markdown(active_description)

            if showOldDescription:
                st.markdown("###### Current Description")
                st.markdown("``` Model Used: Gemini Pro Vision ```")

                desc = fr'''
                {active_description}

                '''
                st.markdown(desc)


