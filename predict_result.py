from tensorflow import keras
import numpy as np
from PIL import Image

def load_saved_model(model_path="resnet152v2_feature_extraction_final_best_model"):
    print('Loading Model at:', model_path)
    model = keras.models.load_model(model_path)
    print('Model Loaded Successfully')
    return model

def read_and_preprocess_image(image_path):
    print('Reading Image from:', image_path)
    im = Image.open(image_path)
    print('Image Loaded Successfully')
    im_shape = np.array(im).shape
    print('Received Image Shape:', im_shape)
    if len(im_shape) != 3:
        raise Exception('Uploaded Image is grayscale(has only 2 color channels) and cannot be processed!')
    if im_shape[2] != 3:
        raise Exception('Uploaded Image is grayscale(has only 2 color channels) and cannot be processed!')
    im = im.resize((224, 224))
    print('Resized Image Shape:', np.array(im).shape)
    return im

def convert_image_to_numpy_array(im):
    x = np.array([
        np.array(im)
    ])
    print('Predict Function Input X Shape:', x.shape)
    return x

# IMPORT & USE THIS FUNCTION
def predict_result(img_path, model = None):
    '''
    PASS THE FULL IMAGE PATH (better not to use relative paths)
    '''
    if model == None:
        model = load_saved_model()
    im = read_and_preprocess_image(img_path)
    x = convert_image_to_numpy_array(im)
    prediction = model.predict(x)
    predicted_proba = prediction[0][0]
    predicted_class = "NORMAL"
    if predicted_proba > 0.5:
        predicted_class = "PNEUMONIA"
    else:
        predicted_proba = (1 - predicted_proba)
    return_dict = {
        'probability': predicted_proba,
        'most_probable_class': predicted_class
    }
    print("Prediction Result:", return_dict)
    return return_dict
    
if __name__ == "__main__":
    res = predict_result('./test_images/normal_1.jpg')
    # res = predict_result('./test_images/pneumonia_1.jpeg')
    # print('Import and use predict_result()')