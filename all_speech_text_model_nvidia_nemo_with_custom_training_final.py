# -*- coding: utf-8 -*-
"""ALL_speech-text_model_nvidia-Nemo_with custom training_final

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1psaPWdjuk3eYyATpRWqi3_bKNhlbK2CG
"""

################---nvidia-Nemo-----------------------------

!pip install nemo_toolkit['all']

import nemo.collections.asr as nemo_asr
asr_model = nemo_asr.models.EncDecCTCModelBPE.from_pretrained("nvidia/stt_en_conformer_ctc_small")

!wget https://dldata-public.s3.us-east-2.amazonaws.com/2086-149220-0033.wav

asr_model.transcribe(['2086-149220-0033.wav'])
#asr_model.transcribe(['/content/Text to speech British accent.mp3'])

#---or------

### Transcribing using Python
MODEL_NAME = "stt_en_conformer_ctc_small"

import nemo.collections.asr as nemo_asr
asr_model = nemo_asr.models.ASRModel.from_pretrained(MODEL_NAME)

!wget https://dldata-public.s3.us-east-2.amazonaws.com/2086-149220-0033.wav

asr_model.transcribe(['2086-149220-0033.wav'])

####################-Open-ai ---WHISPE MODEL

## Install dependencies
!pip install wget
!apt-get install sox libsndfile1 ffmpeg
!pip install text-unidecode
!pip install matplotlib>=3.3.2

data_dir = "/content/audio_data"
output_dir = "/content/audio_data/wav_files"  # Change this to your desired output directory

import glob
import os
import subprocess
import tarfile
import wget

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Download the dataset. This will take a few moments...
print("******")
if not os.path.exists(data_dir + '/an4_sphere.tar.gz'):
    an4_url = 'https://dldata-public.s3.us-east-2.amazonaws.com/an4_sphere.tar.gz'
    an4_path = wget.download(an4_url, data_dir)
    print(f"Dataset downloaded at: {an4_path}")
else:
    print("Tarfile already exists.")
    an4_path = data_dir + '/an4_sphere.tar.gz'

if not os.path.exists(data_dir + '/an4/'):
    # Untar and convert .sph to .wav (using sox)
    tar = tarfile.open(an4_path)
    tar.extractall(path=data_dir)

    print("Converting .sph to .wav...")
    sph_list = glob.glob(data_dir + '/an4/**/*.sph', recursive=True)
    for sph_path in sph_list:
        # Create the output directory structure in wav_files
        relative_path = os.path.relpath(sph_path, data_dir)
        output_wav_path = os.path.join(output_dir, os.path.splitext(relative_path)[0] + '.wav')

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_wav_path), exist_ok=True)

        cmd = ["sox", sph_path, output_wav_path]
        subprocess.run(cmd)
print("Finished conversion.\n******")

!rm -rf "/content/audio_data"
!mkdir "/content/audio_data"



#########-open-ai--whisper model---open source---------------
#https://towardsdatascience.com/speech-to-text-with-openais-whisper-53d5cea9005e

!pip install git+https://github.com/openai/whisper.git -q
import whisper

model = whisper.load_model("large")

text = model.transcribe("/content/audio_data/wav_files/an4/wav/an4_clstk/fmjc/an118-fmjc-b.wav")
#printing the transcribe
text['text']



#------Custom train nvidia nemo--------------------------------------------------------------------------------------------------------------------------------------------

#https://github.com/NVIDIA/NeMo/blob/main/tutorials/asr/ASR_with_NeMo.ipynb

!pip install wget
!apt-get install sox libsndfile1 ffmpeg
!pip install text-unidecode
!pip install matplotlib>=3.3.2

import os
# This is where the an4/ directory will be placed.
# Change this if you don't want the data to be extracted in the current directory.
data_dir = "/content/NvidiaNemo"

if not os.path.exists(data_dir):
  os.makedirs(data_dir)

import glob
import os
import subprocess
import tarfile
import wget

# Download the dataset. This will take a few moments...
print("******")
if not os.path.exists(data_dir + '/an4_sphere.tar.gz'):
    an4_url = 'https://dldata-public.s3.us-east-2.amazonaws.com/an4_sphere.tar.gz'
    an4_path = wget.download(an4_url, data_dir)
    print(f"Dataset downloaded at: {an4_path}")
else:
    print("Tarfile already exists.")
    an4_path = data_dir + '/an4_sphere.tar.gz'

if not os.path.exists(data_dir + '/an4/'):
    # Untar and convert .sph to .wav (using sox)
    tar = tarfile.open(an4_path)
    tar.extractall(path=data_dir)

    print("Converting .sph to .wav...")
    sph_list = glob.glob(data_dir + '/an4/**/*.sph', recursive=True)
    for sph_path in sph_list:
        wav_path = sph_path[:-4] + '.wav'
        cmd = ["sox", sph_path, wav_path]
        subprocess.run(cmd)
print("Finished conversion.\n******")

import librosa
import IPython.display as ipd

# Load and listen to the audio file
example_file = data_dir + '/an4/wav/an4_clstk/mgah/cen2-mgah-b.wav'
audio, sample_rate = librosa.load(example_file)

ipd.Audio(example_file, rate=sample_rate)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import librosa.display
import matplotlib.pyplot as plt

# Plot our example audio file's waveform
plt.rcParams['figure.figsize'] = (15,7)
plt.title('Waveform of Audio Example')
plt.ylabel('Amplitude')

_ = librosa.display.waveshow(audio)

import numpy as np

# Get spectrogram using Librosa's Short-Time Fourier Transform (stft)
spec = np.abs(librosa.stft(audio))
spec_db = librosa.amplitude_to_db(spec, ref=np.max)  # Decibels

# Use log scale to view frequencies
librosa.display.specshow(spec_db, y_axis='log', x_axis='time')
plt.colorbar()
plt.title('Audio Spectrogram');

# NeMo's "core" package
import nemo
# NeMo's ASR collection - this collections contains complete ASR models and
# building blocks (modules) for ASR
import nemo.collections.asr as nemo_asr

# This line will download pre-trained QuartzNet15x5 model from NVIDIA's NGC cloud and instantiate it for you
quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="QuartzNet15x5Base-En")

#Next, we'll simply add paths to files we want to transcribe into the list and pass it to our model. Note that it will work for relatively short (<25 seconds) files.

files = [os.path.join(data_dir, 'an4/wav/an4_clstk/mgah/cen2-mgah-b.wav')]
for fname, transcription in zip(files, quartznet.transcribe(paths2audio_files=files)):
  print(f"Audio in {fname} was recognized as: {transcription}")

'''
Training from Scratch
To train from scratch, you need to prepare your training data in the right format and specify your models architecture.

Creating Data Manifests
The first thing we need to do now is to create manifests for our training and evaluation data, which will contain the metadata of our audio files. NeMo data sets take in a standardized manifest format where each line corresponds to one sample of audio, such that the number of lines in a manifest is equal to the number of samples that are represented by that manifest. A line must contain the path to an audio file, the corresponding transcript (or path to a transcript file), and the duration of the audio sample.

Here's an example of what one line in a NeMo-compatible manifest might look like:

{"audio_filepath": "path/to/audio.wav", "duration": 3.45, "text": "this is a nemo tutorial"}
We can build our training and evaluation manifests using an4/etc/an4_train.transcription and an4/etc/an4_test.transcription, which have lines containing transcripts and their corresponding audio file IDs:

'''

# --- Building Manifest Files --- #
import json

# Function to build a manifest
def build_manifest(transcripts_path, manifest_path, wav_path):
    with open(transcripts_path, 'r') as fin:
        with open(manifest_path, 'w') as fout:
            for line in fin:
                # Lines look like this:
                # <s> transcript </s> (fileID)
                transcript = line[: line.find('(')-1].lower()
                transcript = transcript.replace('<s>', '').replace('</s>', '')
                transcript = transcript.strip()

                file_id = line[line.find('(')+1 : -2]  # e.g. "cen4-fash-b"
                audio_path = os.path.join(
                    data_dir, wav_path,
                    file_id[file_id.find('-')+1 : file_id.rfind('-')],
                    file_id + '.wav')

                duration = librosa.core.get_duration(filename=audio_path)

                # Write the metadata to the manifest
                metadata = {
                    "audio_filepath": audio_path,
                    "duration": duration,
                    "text": transcript
                }
                json.dump(metadata, fout)
                fout.write('\n')

# Building Manifests
print("******")
train_transcripts = data_dir + '/an4/etc/an4_train.transcription'
train_manifest = data_dir + '/an4/train_manifest.json'
if not os.path.isfile(train_manifest):
    build_manifest(train_transcripts, train_manifest, 'an4/wav/an4_clstk')
    print("Training manifest created.")

test_transcripts = data_dir + '/an4/etc/an4_test.transcription'
test_manifest = data_dir + '/an4/test_manifest.json'
if not os.path.isfile(test_manifest):
    build_manifest(test_transcripts, test_manifest, 'an4/wav/an4test_clstk')
    print("Test manifest created.")
print("***Done***")

#Specifying Our Model with a YAML Config File
#For this tutorial, we'll build a Jasper_4x1 model, with K=4 blocks of single (R=1) sub-blocks and a greedy CTC decoder, using the configuration found in ./configs/config.yaml.

#If we open up this config file, we find model section which describes architecture of our model. A model contains an entry labeled encoder, with a field called jasper that contains a list with multiple

# --- Config Information ---#
try:
    from ruamel.yaml import YAML
except ModuleNotFoundError:
    from ruamel_yaml import YAML
config_path = './configs/config.yaml'

if not os.path.exists(config_path):
    # Grab the config we'll use in this example
    BRANCH = 'main'
    !mkdir configs
    !wget -P configs/ https://raw.githubusercontent.com/NVIDIA/NeMo/$BRANCH/examples/asr/conf/config.yaml

yaml = YAML(typ='safe')
with open(config_path) as f:
    params = yaml.load(f)
print(params)

'''
Training with PyTorch Lightning
NeMo models and modules can be used in any PyTorch code where torch.nn.Module is expected.

However, NeMo's models are based on PytorchLightning's LightningModule and we recommend you use PytorchLightning for training and fine-tuning as it makes using mixed precision and distributed training very easy. So to start,
let's create Trainer instance for training on GPU for 50 epochs
'''
import pytorch_lightning as pl
trainer = pl.Trainer(devices=1, accelerator='gpu', max_epochs=250)

from omegaconf import DictConfig
params['model']['train_ds']['manifest_filepath'] = train_manifest
params['model']['validation_ds']['manifest_filepath'] = test_manifest
first_asr_model = nemo_asr.models.EncDecCTCModel(cfg=DictConfig(params['model']), trainer=trainer)

# Start training!!!
trainer.fit(first_asr_model)

#test with validation dataset---------
# Bigger batch-size = bigger throughput
params['model']['validation_ds']['batch_size'] = 16

# Setup the test data loader and make sure the model is on GPU
first_asr_model.setup_test_data(test_data_config=params['model']['validation_ds'])
first_asr_model.cuda()
first_asr_model.eval()

# We will be computing Word Error Rate (WER) metric between our hypothesis and predictions.
# WER is computed as numerator/denominator.
# We'll gather all the test batches' numerators and denominators.
wer_nums = []
wer_denoms = []

# Loop over all test batches.
# Iterating over the model's `test_dataloader` will give us:
# (audio_signal, audio_signal_length, transcript_tokens, transcript_length)
# See the AudioToCharDataset for more details.
for test_batch in first_asr_model.test_dataloader():
        test_batch = [x.cuda() for x in test_batch]
        targets = test_batch[2]
        targets_lengths = test_batch[3]
        log_probs, encoded_len, greedy_predictions = first_asr_model(
            input_signal=test_batch[0], input_signal_length=test_batch[1]
        )
        # Notice the model has a helper object to compute WER
        first_asr_model._wer.update(greedy_predictions, targets, targets_lengths)
        _, wer_num, wer_denom = first_asr_model._wer.compute()
        first_asr_model._wer.reset()
        wer_nums.append(wer_num.detach().cpu().numpy())
        wer_denoms.append(wer_denom.detach().cpu().numpy())

        # Release tensors from GPU memory
        del test_batch, log_probs, targets, targets_lengths, encoded_len, greedy_predictions

# We need to sum all numerators and denominators first. Then divide.
print(f"WER = {sum(wer_nums)/sum(wer_denoms)}")

# Commented out IPython magic to ensure Python compatibility.

#If you'd like to save this model checkpoint for loading later (e.g. for fine-tuning, or for continuing training), you can simply call first_asr_model.save_to(<checkpoint_path>).
## Then, to restore your weights, you can rebuild the model using the config (let's say you call it first_asr_model_continued this time) and call first_asr_model_continued.restore_from(<checkpoint_path>).

#After Training: Monitoring Progress and Changing Hyperparameters
#We can now start Tensorboard to see how training went. Recall that WER stands for Word Error Rate and so the lower it is, the better.

try:
  from google import colab
  COLAB_ENV = True
except (ImportError, ModuleNotFoundError):
  COLAB_ENV = False

# Load the TensorBoard notebook extension
if COLAB_ENV:
#   %load_ext tensorboard
#   %tensorboard --logdir lightning_logs/
else:
  print("To use tensorboard, please use this notebook in a Google Colab environment.")

#We could improve this model by playing with hyperparameters. We can look at the current hyperparameters with the following:

print(params['model']['optim'])

#Let's say we wanted to change the learning rate. To do so, we can create a new_opt dict and set our desired learning rate, then call <model>.setup_optimization() with the new optimization parameters.

import copy
new_opt = copy.deepcopy(params['model']['optim'])
new_opt['lr'] = 0.001
first_asr_model.setup_optimization(optim_config=DictConfig(new_opt))
# And then you can invoke trainer.fit(first_asr_model)

'''
Inference
Let's have a quick look at how one could run inference with NeMo's ASR model.

First, EncDecCTCModel and its subclasses contain a handy transcribe method which can be used to simply obtain audio files' transcriptions. It also has batch_size argument to improve performance.
'''

paths2audio_files = [os.path.join(data_dir, 'an4/wav/an4_clstk/mgah/cen2-mgah-b.wav'),
                     os.path.join(data_dir, 'an4/wav/an4_clstk/fmjd/cen7-fmjd-b.wav'),
                     os.path.join(data_dir, 'an4/wav/an4_clstk/fmjd/cen8-fmjd-b.wav'),
                     os.path.join(data_dir, 'an4/wav/an4_clstk/fkai/cen8-fkai-b.wav')]
print(first_asr_model.transcribe(paths2audio_files=paths2audio_files,
                                 batch_size=4))

paths2audio_files = [os.path.join(data_dir, '/content/2086-149220-0033.wav')]
print(first_asr_model.transcribe(paths2audio_files=paths2audio_files, batch_size=4))

#first_asr_model.save_to("/content/lightning_logs/version_0/checkpoints")

# Save the model checkpoint
# Save the model configuration
model_config_path = '/content/configs/config.yaml'
params['model']['train_ds']['manifest_filepath'] = train_manifest
params['model']['validation_ds']['manifest_filepath'] = test_manifest

with open(model_config_path, 'w') as f:
    yaml.dump(params['model'], f)

# Save the model checkpoint
#checkpoint_path = '/content/lightning_logs/version_0/checkpoints/nemo_asr_checkpoint.ckpt'
checkpoint_path = '/content/lightning_logs/version_1/checkpoints/nemo_asr_checkpoint_retrain.ckpt'

trainer.save_checkpoint(checkpoint_path)

import yaml

# Load the model configuration
with open(model_config_path, 'r') as f:
    model_config = yaml.safe_load(f)

# Create a new trainer for restoring the model
trainer_restore = pl.Trainer(devices=1, accelerator='gpu', max_epochs=250)

# Load the model from the checkpoint
restored_asr_model = nemo_asr.models.EncDecCTCModel(cfg=DictConfig(model_config), trainer=trainer_restore)
restored_asr_model = restored_asr_model.load_from_checkpoint(checkpoint_path)

paths2audio_files = [os.path.join(data_dir, 'an4/wav/an4_clstk/mgah/cen2-mgah-b.wav'),
                     os.path.join(data_dir, 'an4/wav/an4_clstk/fmjd/cen7-fmjd-b.wav'),
                     os.path.join(data_dir, 'an4/wav/an4_clstk/fmjd/cen8-fmjd-b.wav'),
                     os.path.join(data_dir, 'an4/wav/an4_clstk/fkai/cen8-fkai-b.wav')]
print(restored_asr_model.transcribe(paths2audio_files=paths2audio_files,
                                 batch_size=4))

paths2audio_files = [os.path.join(data_dir, '/content/2086-149220-0033.wav')]
print(first_asr_model.transcribe(paths2audio_files=paths2audio_files, batch_size=4))

#Transfer learning

print(quartznet._cfg['spec_augment'])

# Check what kind of vocabulary/alphabet the model has right now
print(quartznet.decoder.vocabulary)
# Let's add "!" symbol there. Note that you can (and should!) change the vocabulary
# entirely when fine-tuning using a different language.
quartznet.change_vocabulary(
    new_vocabulary=[
        ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'", "!"
    ]
)

import copy
new_opt = copy.deepcopy(params['model']['optim'])
new_opt['lr'] = 0.001
first_asr_model.setup_optimization(optim_config=DictConfig(new_opt))

# Use the smaller learning rate we set before
quartznet.setup_optimization(optim_config=DictConfig(new_opt))

# Point to the data we'll use for fine-tuning as the training set
quartznet.setup_training_data(train_data_config=params['model']['train_ds'])

# Point to the new validation data for fine-tuning
quartznet.setup_validation_data(val_data_config=params['model']['validation_ds'])

# And now we can create a PyTorch Lightning trainer and call `fit` again.
trainer = pl.Trainer(devices=1, accelerator='gpu', max_epochs=50)
trainer.fit(quartznet)

#####---speechbrain--------------------------------------------------
#https://huggingface.co/speechbrain
#https://github.com/speechbrain/speechbrain/tree/develop/recipes/CommonVoice/ASR

!pip install speechbrain

from speechbrain.pretrained import EncoderDecoderASR
asr_model =EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-rnnlm-librispeech",
savedir="pretrained_models/asr-crdnn-rnnlm-librispeech")
asr_model.transcribe_file('speechbrain/asr-crdnn-rnnlm-librispeech/example.wav')

!wget https://dldata-public.s3.us-east-2.amazonaws.com/2086-149220-0033.wav
asr_model.transcribe_file('/content/2086-149220-0033.wav')

!git clone https://github.com/speechbrain/speechbrain

#############--facebook wav2vec2-----------------------------------------------------------
#https://huggingface.co/facebook/wav2vec2-large-960h-lv60-self

#!pip install datasets
 from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
 from datasets import load_dataset
 import torch

 # load model and processor
 processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
 model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")

 # load dummy dataset and read soundfiles
 ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")

 # tokenize
 input_values = processor(ds[0]["audio"]["array"], return_tensors="pt", padding="longest").input_values

 # retrieve logits
 logits = model(input_values).logits

 # take argmax and decode
 predicted_ids = torch.argmax(logits, dim=-1)
 transcription = processor.batch_decode(predicted_ids)

# Load a single .wav file
# Import necessary libraries
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch, torchaudio

wav_file_path = "/content/2086-149220-0033.wav"
audio_input, _ = torchaudio.load(wav_file_path, normalize=True)

# Tokenize
input_values = processor(audio_input.squeeze().numpy(), return_tensors="pt", padding="longest").input_values

# Retrieve logits
logits = model(input_values).logits

# Take argmax and decode
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)

# Print the transcription
print("Transcription:", transcription[0])

