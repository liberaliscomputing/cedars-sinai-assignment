#!/usr/bin/env python
from itertools import groupby
import re
import os

import pandas as pd


def parse_fasta(fasta_file_path):
    """Parse a FASTA file

    :param fasta_file_path: A path to a fasta file with protein sequences
    :type fasta_file_path: str
    :return: A list of protein name and sequence pairs
    :rtype: list
    """
    protein_sequences = []

    with open(fasta_file_path, "rb") as f:
        iterator = (
            group for _, group in groupby(f, lambda line: str(line, "utf-8")[0] == ">")
        )
        for header in iterator:
            protein_name = str(header.__next__(), "utf-8").strip().replace(">", "")
            sequence = "".join(str(s, "utf-8").strip() for s in iterator.__next__())
            protein_sequences.append(
                {"ProteinName": protein_name, "Sequence": sequence}
            )

    return protein_sequences


def run(input_file_path, fasta_file_path, output_file_path, file_format):
    """Find post-translational modifications (PTMs).

    :param input_file_path: A path to an input file with a list of peptide sequences
    :type input_file_path: str
    :param fasta_file_path: A path to a fasta file with protein sequences
    :type fasta_file_path: str
    :param output_file_path: A path to an output file
    :type output_file_path: str
    :param file_format: A file format to read in an input file and write out to an output file, defaults to tsv
    :type file_format: str
    """
    # 1. Read in input file
    full_peptide_names = []
    header = False

    with open(input_file_path, "rb") as f:
        for line in f:
            s = str(line.strip(), "utf-8")
            if not header:
                header = True
                continue
            full_peptide_names.append(s)

    full_peptide_names = list(set(full_peptide_names))

    # 2. Read in fasta file
    protein_sequences = parse_fasta(fasta_file_path)

    # 3. Find modified amino acid positions
    results = []

    # Loop over protein sequences
    for protein_sequence in protein_sequences:
        protein_name = protein_sequence["ProteinName"]
        sequence = protein_sequence["Sequence"]

        # Loop over full peptide names
        for full_peptide_name in full_peptide_names:

            # Apply the lines below only if a modification(s) found
            if "UniMod" in full_peptide_name:

                # Remove (UniMod:[0-9]+) from full peptide name
                pattern = full_peptide_name
                for match in re.compile("\(UniMod:[0-9]+\)").finditer(
                    full_peptide_name
                ):
                    pattern = pattern.replace(match.group(), "")

                # Find full peptide name from protien sequence
                for match in re.compile(pattern).finditer(sequence):
                    results.append(
                        {
                            "ProteinName": protein_name,
                            "FullPeptideName": full_peptide_name,
                            "StartsAt": match.start(),
                            "EndsAt": match.end(),
                        }
                    )

    # Write to output file
    sep = "\t" if file_format == "tsv" else ","
    pd.DataFrame(results).to_csv(
        os.path.join(output_file_path, f"results.{file_format}"), sep=sep, index=False
    )
