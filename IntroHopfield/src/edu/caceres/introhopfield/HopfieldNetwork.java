package edu.caceres.introhopfield;

public class HopfieldNetwork {

    private Matrix weightMatrix;

    public HopfieldNetwork(int numNeurons) {
        this.weightMatrix = new Matrix(numNeurons, numNeurons);
    }

    public Matrix getWeightMatrix() {
        return this.weightMatrix;
    }

    public int getSize() {
        return this.weightMatrix.getRows();
    }

    public boolean[] present(final boolean[] pattern) {
        // the parameter and output are boolean matrices where each false represents 0 and each true represents 1.
        final boolean[] output = new boolean[pattern.length];

        // convert the input pattern into a matrix with a single row.
        // also convert the boolean values to bipolar(0 --> -1=false, 1 --> 1=true)
        final Matrix inputMatrix = Matrix.createRowMatrix(BiPolarUtil.boolToBipolar(pattern));

        // For each neuron in the network (each column --> what the neuron receives), calculate its final product.
        for (int col = 0; col < pattern.length; col++) {
            Matrix columnMatrix = this.weightMatrix.getCol(col);
            columnMatrix = MatrixMath.transpose(columnMatrix);

            // The output for this neuron is the dot product of the input matrix and one column from the weight matrix.
            // The dot product is the result because each weight in the column
            // corresponds to the input to that neuron in the pattern matrix.
            final double dotProduct = MatrixMath.dotProduct(inputMatrix,
                    columnMatrix);

            // Convert the dot product to either true or false.
            output[col] = dotProduct > 0;
        }

        return output;
    }

    public void train(final boolean[] pattern) {
        if(pattern.length != weightMatrix.getRows())
            throw new IllegalArgumentException("Can't train a pattern of size "
                    + pattern.length + " on a hopfield network of size "
                    + this.weightMatrix.getRows());
        // this calculates the weight matrix that matches the pattern
        final Matrix rowInput = Matrix.createRowMatrix(BiPolarUtil.boolToBipolar(pattern));
        final Matrix colInput = MatrixMath.transpose(rowInput);
        final Matrix input = MatrixMath.matrixMultiply(colInput, rowInput); // this matrix is square

        // need to subtract identity matrix to cancel out 1s in top-left diagonal
        final Matrix identity = Matrix.createIdentityMatrix(input.getRows());
        final Matrix weights = MatrixMath.add(input, identity, true);

        this.weightMatrix = MatrixMath.add(this.weightMatrix, weights, false);
    }
}
