# FeatureLayers

## Installation
```bash
pip install featurelayers
```


## Usage
### LBC Layers
```python
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from featurelayers.layers.LBC import LBC

# Create a simple Keras model
model = Sequential()
# Add the LBC layer as the first layer in the model
model.add(LBC(filters=32, kernel_size=3, stride=1, padding='same', activation='relu', sparsity=0.9, name='lbc_layer'))
# Add a Flatten layer to convert the output to 1D
model.add(Flatten())
# Add a Dense layer for classification
model.add(Dense(units=10, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Generate some dummy data
x_train = np.random.rand(100, 28, 28, 1)
y_train = np.random.randint(0, 10, size=(100,))

# Convert the labels to one-hot encoding
y_train = keras.utils.to_categorical(y_train, num_classes=10)

# Train the model
model.fit(x_train, y_train, epochs=10, batch_size=32)

```

__version__ = ""1.4.3""