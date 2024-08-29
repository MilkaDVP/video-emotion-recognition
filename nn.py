import numpy as np
import random
import copy
def sigmoid(x):
	return 1 / (1 + np.exp(-x))
def sigmoid_derivative(x):
	return x * (1 - x)
def relu(x):
	return np.maximum(0, x)

def relu_derivative(x):
	return np.where(x > 0, 1, 0)

def tanh(x):
	return np.tanh(x)

def tanh_derivative(x):
	return 1 - x**2

def step(x):
	return np.where(x >= 0.5, 1, 0)

def step_derivative(x):
	return np.ones_like(x)

def linear(x):
	return x

def linear_derivative(x):
	return np.ones_like(x)

def softmax(x):
	exp_x = np.exp(x - np.max(x))
	return exp_x / exp_x.sum(axis=0, keepdims=True)

def softmax_derivative(x):
	s = softmax(x)
	return s * (1 - s)
activation_functions = {
    sigmoid: sigmoid_derivative,
    relu: relu_derivative,
    tanh: tanh_derivative,
	step:step_derivative,
	linear:linear_derivative,
	softmax:softmax_derivative
}

class NeuralNetwork:
	def __init__(self, layers):
		self.layers = layers
		self.num_layers = len(layers)
		self.weights = [np.random.randn(layers[i-1][0], layers[i][0]) for i in range(1, self.num_layers)]
		self.biases = [np.random.randn(1, layers[i][0]) for i in range(1, self.num_layers)]
		self.activations = [activation for _,activation in layers]
		self.activation_derivatives = [activation_functions[activation] for activation in self.activations]
		self.reversed=False
	def _forward(self, x):
		output = np.array(x)
		for i in range(self.num_layers - 1):
			if self.reversed and self.activations[i]==sigmoid:
				z = np.dot(reversedigmoid(output)-self.biases[i][0], self.weights[i])
			else:
				z = np.dot(output, self.weights[i]) + self.biases[i]
			output = self.activations[i](z)
		return output
	def predict(self, x):
		a= self._forward(x)
		if len(a[0])>1:
			return a
		else:
			return a[0::,0]
	def train(self, x_train, y_train, learning_rate=0.1, num_epochs=1000, echo=False):
		for epoch in range(num_epochs):
			for x, y in zip(x_train, y_train):
				x = np.array(x).reshape(1, -1)
				if type(y)!=list:
					y = np.array(y).reshape(1, -1)
				# Forward propagation
				layer_outputs = [x]
				for i in range(self.num_layers - 1):
					if self.reversed:
						z = np.dot(layer_outputs[i]+self.biases[i], self.weights[i])
					else:
						z = np.dot(layer_outputs[i], self.weights[i]) + self.biases[i]
					output = self.activations[i](z)
					layer_outputs.append(output)
				# Backpropagation
				if type(y)!=list:
					error = layer_outputs[-1] - y
				else:
					error=layer_outputs[-1].tolist()[0]
					for i in range(len(error)):
						if y[i]==None:
							error[i]=0
						else:
							error[i]=layer_outputs[-1][0][i]-y[i]
					error=np.array([error])
				for i in range(self.num_layers - 2, -1, -1):
					activation_derivative = self.activation_derivatives[i](layer_outputs[i+1])
					delta = error * activation_derivative
					self.weights[i] -= learning_rate * np.dot(layer_outputs[i].T, delta)
					self.biases[i] -= learning_rate * delta

					error = np.dot(delta, self.weights[i].T)

			if echo:
				mse,predicts = self.evaluate(x_train, y_train)
				print(f"Epoch {epoch+1}, Mean Squared Error: {mse}")
		if echo:
			return predicts
	def evaluate(self, x_test, y_test):
		predictions = [self.predict(x) for x in x_test]
		y_test1=[]
		for i in range(len(y_test)):
			a=[]
			for j in range(len(y_test[i])):
				if y_test[i][j]==None:
					try:
						a.append(predictions[i][j])
					except:
						a.append(predictions[i][0][j])
				else:
					a.append(y_test[i][j])
			y_test1.append(a)
		y_test1=np.array(y_test1)
		mse = np.mean([(pred - y)**2 for pred, y in zip(predictions, y_test1)])
		return mse,predictions
	def copy(self):
		return copy.deepcopy(self)
	def mutate(self, mutation_rate=0.1, mutation_range=0.5):
		for i in range(self.num_layers - 1):
			mutation_mask = np.random.rand(*self.weights[i].shape) < mutation_rate
			self.weights[i][mutation_mask] += np.random.uniform(-mutation_range, mutation_range, size=self.weights[i].shape)[mutation_mask]
			mutation_mask = np.random.rand(*self.biases[i].shape) < mutation_rate
			self.biases[i][mutation_mask] += np.random.uniform(-mutation_range, mutation_range, size=self.biases[i].shape)[mutation_mask]
	def divide(self,idlayer):
		a=self.copy()
		b=self.copy()
		a.layers=a.layers[0:idlayer+1]
		a.weights=a.weights[0:idlayer]
		a.biases=a.biases[0:idlayer]
		a.activations=a.activations[0:idlayer+1]
		a.activation_derivatives=a.activation_derivatives[0:idlayer+1]
		a.num_layers=len(a.layers)
		b.layers=b.layers[idlayer::]
		b.weights=b.weights[idlayer::]
		b.biases=b.biases[idlayer::]
		b.activations=b.activations[idlayer+1::]
		b.activation_derivatives=b.activation_derivatives[idlayer+1::]
		b.num_layers=len(b.layers)
		return a,b
	def reversedpredict(self,outputs):
		for i in range(self.num_layers - 2, -1, -1):
			outputs = self.activations[i-1](np.dot(outputs, self.weights[i].T)+self.biases[i-1])
		return outputs
	def geterror(self,x,y,layerid):
		x = np.array(x).reshape(1, -1)
		if type(y)!=list:
			y = np.array(y).reshape(1, -1)
		# Forward propagation
		layer_outputs = [x]
		for i in range(self.num_layers - 1):
			if self.reversed:
				z = np.dot(layer_outputs[i]+self.biases[i], self.weights[i])
			else:
				z = np.dot(layer_outputs[i], self.weights[i]) + self.biases[i]
			output = self.activations[i](z)
			layer_outputs.append(output)
		# Backpropagation
		if type(y)!=list:
			error = layer_outputs[-1] - y
		else:
			error=layer_outputs[-1].tolist()[0]
			for i in range(len(error)):
				if y[i]==None:
					error[i]=0
				else:
					error[i]=layer_outputs[-1][0][i]-y[i]
			error=np.array([error])
		for i in range(self.num_layers - 2, layerid-1, -1):
			activation_derivative = self.activation_derivatives[i](layer_outputs[i+1])
			delta = error * activation_derivative
			error = np.dot(delta, self.weights[i].T)
		return error