# MIT License
#
# Copyright (c) 2020 International Business Machines
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json

class Arguments:
     """This class defines the user arguments object, and sets the default values for some parameters"""
     def __init__(self, model, dataset_name, classes, num_epochs, data_dir):
         self.model = model
         self.dataset_name = dataset_name
         self.classes = classes
         self.num_epochs = num_epochs
         self.data_dir = data_dir #path to dataset
         
         #defaults:
         self.seed=123  #select seed number for reproducibility
         self.lr=0.001  #learning rate
         self.batch_size = 200
         self.opt='adam'
         self.save_dir='outputs/mltoolbox/'                     #path to checkpoint save directory
         self.save_freq=-1                        #how frequently save checkpoint (-1: overwrite last checkpoint each period; 0:  do not save; positive integer: write checkpoint for a given freq only)
         self.pooling_type="avg"  #max or average pooling, choices=('max', 'avg')
         self.activation_type="relu_range_aware"   #activation type', choices=('non_trainable_poly', 'trainable_poly', 'approx_relu', 'relu', 'square', 'relu_range_aware', 'weighted_relu'))
         self.debug_mode=False         #breaks a training epoch after loading only a few batches.
         self.replace_all_at_once=True   #changes the activation layers at once or layer by layer
         self.epoch_to_start_change=-1     #epoch number to start changing the activation function (set to -1 when it is not utilized, the change is performed on the first epoch)
         self.change_round=-1              #number of epochs per change (set to -1 when it is not utilized)
         self.smooth_transition=False      #change each activation layer in a smooth change or at once
         self.gradient_clip=-1.0          #gradient clipping value
         self.change_bn_or_add=True
         self.bn_before_activation=False
         self.log_string='test'
         self.from_checkpoint=''          #location of .pth checkpoint file to load. If empty the model will be created from scratch
         self.coeffs_scale=[[0.1, 0.1, 0],[1.,1., 1]]  #coefficients scale for trainable poly activation optionally including initial value of coefs
         self.distillation_path=""               #path for a distillation model file
         self.distillationT=10.0
         self.distillation_alpha=0.1
         self.continue_with_nans=False
         self.local_rank=0
         self.ddp=False
         self.ffcv=False          #using ffcv improves running speed, but reqires converting the data into supported format and pointing to it in ffcv_train_data_path argument
         self.distillation_model=None
         self.lr_new=0.0002
         self.validation_freq=1
         self.disable_scheduler=False
         self.min_lr = 1e-5         # minimal learning rate for scheduler
         self.ffcv_train_data_path = ""    #location of ffcv data. Required if ffcvis set to True
         self.range_aware_train = False
         self.range_awareness_loss_weight = 0     #weight of range awareness loss term in the loss function
         self.poly_degree = 18

     def dump_to_file(self, path):
        with open(os.path.join(path, 'training_arguments.json'), 'w') as f:
            json.dump(self.__dict__, f, indent=2, default=lambda x: str(type(x)))