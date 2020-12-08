#!/usr/bin/env python 
import io
import json
import os
import base64

import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request

# set environ for pytorch 
os.environ['TORCH_HOME'] = 'model_dir/checkpoints'

app = Flask(__name__)

# model using densenet / vgg16
model = models.densenet121(pretrained=True)  
model.eval()

print('done loading pre-train datasets')

img_class_map = None
mapping_file_path = 'index_to_name.json'

if os.path.isfile(mapping_file_path):
    with open (mapping_file_path) as f:
        img_class_map = json.load(f)

# misc 
# image transformation 
def transform_image(infile):
    input_transforms = [transforms.Resize(255),           
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],       
            [0.229, 0.224, 0.225])]
    my_transforms = transforms.Compose(input_transforms)
    # image opening (PIL)
    image = Image.open(infile)                            
    timg = my_transforms(image)                           
    timg.unsqueeze_(0)                                   
    return timg


# Get a prediction
def get_prediction(input_tensor):
    outputs = model.forward(input_tensor)                 
    _, y_hat = outputs.max(1)                             
    prediction = y_hat.item()                             
    return prediction

# map prediction class
def render_prediction(prediction_idx):
    stridx = str(prediction_idx)
    class_name = 'Unknown'
    if img_class_map is not None:
        if stridx in img_class_map is not None:
            class_name = img_class_map[stridx][1]

    return prediction_idx, class_name

@app.route('/', methods=['GET'])
def root():
    return jsonify({'msg' : 'Try POSTing to the /predict endpoint with an RGB image attachment'})


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file is not None:
            img_base64 = base64.b64encode(file.read())
            input_tensor = transform_image(file)
            prediction_idx = get_prediction(input_tensor)
            class_id, class_name = render_prediction(prediction_idx)

            return jsonify(
                    {
                        'class_id': class_id, 
                        'class_name': class_name,
                        'img_base64': str(img_base64.decode('ascii'))
                    }
                )
