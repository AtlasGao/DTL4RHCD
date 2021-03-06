import theano
import theano.tensor as T
from .HiddenLayer import HiddenLayer
from theano.ifelse import ifelse
import numpy as np

class DropoutHiddenLayer(HiddenLayer):
    def __init__(self, rng, input, n_in, n_out, is_train,
                 activation, dropout_rate, mask=None, W=None, b=None):
        super(DropoutHiddenLayer, self).__init__(
                rng=rng, input=input, n_in=n_in, n_out=n_out, W=W, b=b,
                activation=activation)

        self.dropout_rate = dropout_rate
        self.srng = T.shared_randomstreams.RandomStreams(rng.randint(999999))
        self.mask = mask
        self.layer_output = self.output

        # Computes outputs for train and test phase applying dropout when needed.
        # train_output = self.layer_output * T.cast(self.mask, theano.config.floatX)
        train_output = self.drop(self.layer_output, self.dropout_rate)
        test_output = self.output * (1 - dropout_rate)
        self.output = ifelse(T.eq(is_train, 1), train_output, test_output)
        return

    def drop(self, input, p=0.5):
        """
        :type input: numpy.array
        :param input: layer or weight matrix on which dropout resp. dropconnect is applied

        :type p: float or double between 0. and 1.
        :param p: p probability of NOT dropping out a unit or connection, therefore (1.-p) is the drop rate.
        """

        mask = self.srng.binomial(n=1, p=p, size=input.shape, dtype=theano.config.floatX)
        return input * mask

