import nn
import numpy as np
class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(x, self.w)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        return 1 if nn.as_scalar(nn.DotProduct(x, self.w)) >= 0 else -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 1
        while True:
            noerror = True
            for x, y in dataset.iterate_once(batch_size):
                if self.get_prediction(x) != nn.as_scalar(y):
                    self.w.update(x, nn.as_scalar(y))
                    noerror = False
            
            if noerror:
                break
                
class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 1
        self.hidden_layer_size = 30
        self.learning_rate = -0.004

        self.weights1 = nn.Parameter(1, self.hidden_layer_size)
        self.bias1 = nn.Parameter(1, self.hidden_layer_size)
        self.weightsout = nn.Parameter(self.hidden_layer_size, 1)
        self.biasout = nn.Parameter(1, 1)
        
    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        w1 = nn.Linear(x, self.weights1)
        out1 = nn.ReLU(nn.AddBias(w1, self.bias1))
        wout = nn.Linear(out1, self.weightsout)
        return nn.AddBias(wout, self.biasout)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)


    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:

            for x,y in dataset.iterate_once(self.batch_size):
                Del = nn.gradients(self.get_loss(x,y), [self.weights1, self.bias1, self.weightsout, self.biasout])

                self.weights1.update(Del[0], self.learning_rate)
                self.bias1.update(Del[1], self.learning_rate)
                self.weightsout.update(Del[2], self.learning_rate)
                self.biasout.update(Del[3], self.learning_rate)

            b = nn.as_scalar(self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y)))

            if b <= 0.02:
                break
        

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 1
        self.inputdim = 784
        self.hidden_layer_size = 125
        self.learning_rate = -0.008

        self.weights1 = nn.Parameter(self.inputdim, self.hidden_layer_size)
        self.bias1 = nn.Parameter(1, self.hidden_layer_size)
        self.weightsout = nn.Parameter(self.hidden_layer_size, 10)
        self.biasout = nn.Parameter(1, 10)
        
    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        w1 = nn.Linear(x, self.weights1)
        out1 = nn.ReLU(nn.AddBias(w1, self.bias1))
        wout = nn.Linear(out1, self.weightsout)
        return nn.AddBias(wout, self.biasout)

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)
    
    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:

            for x,y in dataset.iterate_once(self.batch_size):
                Del = nn.gradients(self.get_loss(x,y), [self.weights1, self.bias1, self.weightsout, self.biasout])

                self.weights1.update(Del[0], self.learning_rate)
                self.bias1.update(Del[1], self.learning_rate)
                self.weightsout.update(Del[2], self.learning_rate)
                self.biasout.update(Del[3], self.learning_rate)


            if dataset.get_validation_accuracy() >= 0.97:
                break
                
class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 100
        self.w1 = nn.Parameter(self.num_chars, 200)
        self.w2 = nn.Parameter(200, 200)
        self.w3 = nn.Parameter(1, 200)
        self.w4 = nn.Parameter(200, 5)
        self.w5 = nn.Parameter(1, 5)
        self.learning_rate = -0.1
        
        
    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        temp0 = len(xs)
        temp = range(1, temp0)
        temp6 = nn.Linear(xs[0], self.w1)
        temp5 = nn.AddBias(temp6 , self.w3)
        temp1 = nn.ReLU(temp5)
        for x in temp:
            c = nn.Linear(xs[x], self.w1)
            d = nn.Linear(temp1, self.w2)
            b = nn.Add(c , d)
            a = nn.AddBias(b , self.w3)
            temp1 = nn.ReLU(a)


        e = nn.Linear(temp1, self.w4)
        f = nn.AddBias(e, self.w5)
        
        return f
    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(xs), y)
    
    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        temp = dataset.iterate_forever(self.batch_size)
        for x,y in temp:
            temp1 = nn.gradients(self.get_loss(x,y), [self.w1, self.w2, self.w3, self.w4, self.w5])
            self.w1.update(temp1[0], self.learning_rate)
            self.w2.update(temp1[1], self.learning_rate)
            self.w3.update(temp1[2], self.learning_rate)
            self.w4.update(temp1[3], self.learning_rate)
            self.w5.update(temp1[4], self.learning_rate)
            if dataset.get_validation_accuracy() >= 0.89:
                return
            
            