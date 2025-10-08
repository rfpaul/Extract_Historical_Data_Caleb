## Set up model

from PIL import Image
from glob import glob
from os import path
import requests

from transformers import AutoModelForCausalLM
from transformers import AutoProcessor

model_id = "microsoft/Phi-3.5-vision-instruct"

# Note: set _attn_implementation='eager' if you don't have flash_attn installed
model = AutoModelForCausalLM.from_pretrained(
  model_id,
  device_map="cuda",
  trust_remote_code=True,
  torch_dtype="auto",
  _attn_implementation='flash_attention_2'
)

# for best performance, use num_crops=4 for multi-frame, num_crops=16 for single-frame.
processor = AutoProcessor.from_pretrained(model_id,
  trust_remote_code=True,
  num_crops=16
)

## Set up input and output directories, prompts, etc.
# Change this to the file type extension of the output responses
file_ext = 'json'

# Helper function to get the prototype responses to the prototye images and turn
# them into the full prompt; change the prompt constructors as needed for your
# own data extraction needs
def Promptify_Proto_Image_Paths(path_list):
    messages = []

    for i, p in enumerate(path_list, start=1):
        # Drop the file extension and split apart the path
        full_path_split = path.splitext(p)[0].split(path.sep)
        # Change the parent directory to the prototype response directory
        full_path_split[-2] = "Prototype Responses"
        # Recombine to get the path to the prototype responses
        proto_response_path = path.sep.join(full_path_split) + f'.{file_ext}'
        # Get the proto response contents as a string
        with open(proto_response_path, 'r') as f:
            proto_response = f.read()

        if i == 1:
            messages.extend(
                [
                    {"role": "user", "content": "<|image_1|>\nI'm digitizing historical reports of problem sites around mined-out areas and abandoned mines in Illinois. Township, Range, and Section are PLSS bearings. I need you to extract all the textual and numeric data into JSON format. Represent numerical values as standard US decimal numbers with no thousands separators. The fields 'Owner', 'Mined_by' and 'Photo_Reference' occassionally wrap to a second line. Represent blank, empty, or NA values as {}."},
                    {"role": "assistant", "content": proto_response}
                ])
        else:
            messages.extend(
                [
                    {"role": "user", "content": f"<|image_{i}|>\nExtract all the textual and numeric data from this image in JSON format."},
                    {"role": "assistant", "content": proto_response}
                ])

        # If we're on the last path, append the prompt for the infer image
        if i == len(path_list):
            messages.append({"role": "user", "content": f"<|image_{i+1}|>\nExtract all the textual and numeric data from this image in JSON format."})

    return messages

# Prototype images to guide response
proto_img_paths = [
   r"C:\Your\prototype\image\here\001.png",
    r"C:\Your\prototype\image\here\002.png"
    ]

# Create inference prompt from prototype images & their associated JSONs
messages = Promptify_Proto_Image_Paths(proto_img_paths)

# List of images; these first images are the prototype images
image_list = [Image.open(p) for p in proto_img_paths]
# Add a placeholder for the infer image
image_list.append(None)

# Directory + search wildcard location of the images to extract data from
extract_img_pattern = r"C:\Your\historical\document\image\location\here\*.png"

# Directory + search wildcard location of the final, verified outputs
extract_complete_pattern = r"C:\Your\final\verified\output\files\here\*." + f'{file_ext}'

# Output directory for response exports with string formatting placeholder
dest_dir = r"C:\Your\export\location\here\{}." + f'{file_ext}'

# Paths of complete and verified response outputs
complete_paths = glob(extract_complete_pattern)
# Complete sites, filename only without file extension
complete_names = [path.basename(path.splitext(p)[0]) for p in complete_paths]

# Paths for all the inference images to extract
extract_img_paths = glob(extract_img_pattern)
# ...Minus the completed extractions
extract_img_paths = [p for p in extract_img_paths if path.basename(path.splitext(p)[0]) not in complete_names]
extract_img_paths.sort()

## Main script run

prompt = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

for img_path in extract_img_paths:
    with Image.open(img_path) as infer_img:
        # Put the infer image at the end of the image list
        image_list[-1] = infer_img

        inputs = processor(prompt, image_list, return_tensors="pt").to("cuda:0")

        generation_args = {
            "max_new_tokens": 512,
            "do_sample": False
        }

        generate_ids = model.generate(**inputs, eos_token_id=processor.tokenizer.eos_token_id, **generation_args)

        # remove input tokens
        generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
        response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        filename = path.basename(path.splitext(img_path)[0])
        with open(dest_dir.format(filename), 'w') as f:
            f.write(response)
            print(f"Wrote data extraction inference to {filename}.{file_ext}")
