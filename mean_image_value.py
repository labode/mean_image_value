import argparse
import time
import converter
import nrrd
import numpy as np
import os
import csv_writer


def analyze(file):
    # Read .nrrd
    data, header = nrrd.read(file)

    # Create array for results
    results = []

    mean_including_background = data.mean()
    print("Mean image value including background = " + str(mean_including_background))
    results.append(["Mean image value including background", mean_including_background])

    mean_without_background = data[np.nonzero(data)].mean()

    print("Mean image value excluding background = " + str(mean_without_background))
    results.append(["Mean image value excluding background", mean_without_background])

    return results


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculates the mean value of all non zero voxels in a .mha file')
    parser.add_argument('input_file', action='store', type=str, help='.mha file to analyze')
    parser.add_argument('-o', '--output_file', action='store', type=str, default='analysis.csv', required=False,
                        help='Name of output file; Default: analysis.csv')

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file

    # create name for .nrrd that is unique enough not to cause accidental conflicts
    nrrd_tmpfile = 'volume_' + str(int(time.time()))

    # Convert volume to .nrrd
    print('Converting .mha to .nrrd')
    nrrd_file = converter.convert(input_file, nrrd_tmpfile)
    print('Temp .nrrd file written to ' + nrrd_tmpfile + '.nrrd')

    # Analyze .nrrd
    print('Analysing .nrrd')
    analysis = analyze(nrrd_file)

    # Cleanup
    print('Removing temp file')
    os.remove(nrrd_tmpfile + '.nrrd')

    # Write .csv with the results
    print('Writing analysis to .csv')
    csv_writer.write(analysis, output_file)
