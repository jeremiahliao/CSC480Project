import librosa
import numpy as np
from openai import OpenAI
import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def extract_features(wav_file):
    y, sr = librosa.load(wav_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=1)
    return mfccs.T

def reduce_features(features, n_components=None):
    n_samples, n_features = features.shape
    if n_components is None or n_components > min(n_samples, n_features):
        n_components = min(n_samples, n_features)
    pca = PCA(n_components=n_components)
    reduced_features = pca.fit_transform(features)
    return reduced_features

def get_embeddings(features):
    features_flat = f"{features.flatten().tolist()}"
    return client.embeddings.create(input=features_flat, model="text-embedding-3-small").data[0].embedding

def save_embeddings_with_names(embeddings_dict, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(embeddings_dict, f)

def load_embeddings_with_names(file_name):
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        with open(file_name, 'rb') as f:
            embeddings_dict = pickle.load(f)
    else:
        embeddings_dict = {}
    return embeddings_dict

def compute_similarity_with_names(input_embedding, embeddings_dict):
    if not embeddings_dict:
        return [], []
    names = list(embeddings_dict.keys())
    embeddings = np.array(list(embeddings_dict.values()))
    input_embedding = np.array(input_embedding).reshape(1, -1)
    similarities = cosine_similarity(input_embedding, embeddings)[0]
    return names, similarities

def find_most_similar_with_names(input_embedding, embeddings_dict, top_n=5):
    names, similarities = compute_similarity_with_names(input_embedding, embeddings_dict)
    if not similarities:
        return [], []
    most_similar_indices = np.argsort(similarities)[-top_n:][::-1]
    most_similar_names = [names[i] for i in most_similar_indices]
    most_similar_scores = similarities[most_similar_indices]
    return most_similar_names, most_similar_scores

def checkSimilarity(wavData):
    new_features = extract_features(wavData)
    reduced_features = reduce_features(new_features)
    input_embedding = get_embeddings(reduced_features)
    pickle_file = 'embeddings_with_names.pkl'
    embeddings_dict = load_embeddings_with_names(pickle_file)
    most_similar_names, most_similar_scores = find_most_similar_with_names(input_embedding, embeddings_dict, top_n=5)
    similarity_map = {most_similar_names[i]: most_similar_scores[i] for i in range(len(most_similar_names))}
    return similarity_map

def saveNew(name, wavData):
    new_features = extract_features(wavData)
    reduced_features = reduce_features(new_features)
    input_embedding = get_embeddings(reduced_features)
    pickle_file = 'embeddings_with_names.pkl'
    embeddings_dict = load_embeddings_with_names(pickle_file)
    embeddings_dict[name] = input_embedding
    save_embeddings_with_names(embeddings_dict, pickle_file)
