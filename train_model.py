

import numpy as np
from alexnet import alexnet

width = 80
height = 60

LR = 1e-3
EPOCHS = 8

MODEL_NAME = 'pyets2-volvo-{}-{}-{}-{}-epochs.model'.format(LR, 'alexnet', EPOCHS,"v2")

model = alexnet(width, height, LR)

train_data = np.load('training_data/training_data_balanced_v2.npy')

train = train_data[:-500]
test = train_data[-500:]

X = np.array([i[0] for i in train]).reshape(-1,width, height, 1) #i[0] to obraz
Y = [i[1] for i in train]

test_x = np.array([i[0] for i in test]).reshape(-1,width, height, 1) #i[0] to obraz
test_y = [i[1] for i in test]

model.fit({'input':X},{'targets':Y}, n_epoch = EPOCHS, validation_set = ({'input':test_x},{'targets':test_y}),
    snapshot_step=500, show_metric = True, run_id=MODEL_NAME)

# tensorboard --logdir=foo:C:/Users/micha/Documents/ETS 2 autosterowanie/log

model.save(MODEL_NAME)