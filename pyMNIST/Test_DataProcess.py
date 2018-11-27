import NetTrainerTester as Processor

inputs = [[0, 0, 145, 164, 255, 56, 83],
          [1, 3, 98, 231, 0, 57, 32],
          [5, 93, 24, 133, 241, 200, 0]]
new_inputs = Processor.process_input_data(inputs)
outputs = [1, 8, 4]
new_outputs = Processor.process_output_data(outputs)

if __name__ == "__main__":
    print([new_inputs], "\n\n")
    print([new_outputs])
