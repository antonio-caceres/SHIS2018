import NetTrainerTester as Processor

inputs = [[0, 0, 145, 164, 255, 56, 83],
          [1, 3, 98, 231, 0, 57, 32],
          [5, 93, 24, 133, 241, 200, 0]]
new_inputs = Processor.process_input_data(inputs)
print([new_inputs], "\n\n")

outputs = [1, 8, 4]
new_outputs = Processor.process_output_data(outputs)
print([new_outputs])
