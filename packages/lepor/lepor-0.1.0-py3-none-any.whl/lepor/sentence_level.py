import math
import re


def length_penalty(reference, output):
    """
    Function will calculate length penalty(LP) in score due to difference in lengths.

    Args:
        reference: reference sentence
        output: output sentence by a translation engine.
    Return:
        LP: penalty of difference in length in reference and output sentence.
    """

    r_len = len(reference)
    o_len = len(output)

    if r_len == o_len:
        return 1
    elif r_len < o_len:
        return math.exp(1 - (r_len/o_len))
    else:
        return math.exp(1 - (o_len/r_len))


def ngram_positional_penalty(ref_words, out_words):
    """
    Function will calculate

    Args:
        ref_words: reference sentence
        out_words: output sentence by a translation engine.
    Return:
        NPosPenal: penalty due to difference in positions of ngram in reference and output sentences.
    """

    alignments = []

    for out_index, out_word in enumerate(out_words):
        if ref_words.count(out_word) == 0:
            alignments.append(-1)
        elif ref_words.count(out_word) == 1:
            alignments.append(ref_words.index(out_word))
        else:
            # if there are multiple possibilities.
            ref_indexes = [i for i, word in enumerate(ref_words) if word == out_word]

            is_matched = [False] * len(ref_indexes)

            for ind, ref_word_index in enumerate(ref_indexes):
                if 0 < ref_word_index - 1 < len(ref_words) and 0 < out_index - 1 < len(out_words) \
                        and ref_words[ref_word_index - 1] == out_words[out_index - 1]:
                    is_matched[ind] = True
                elif 0 < ref_word_index + 1 < len(ref_words) and 0 < out_index + 1 < len(out_words) \
                        and ref_words[ref_word_index + 1] == out_words[out_index + 1]:
                    is_matched[ind] = True

            if is_matched.count(True) == 1:
                alignments.append(ref_indexes[is_matched.index(True)])
            elif is_matched.count(True) > 1:
                min_distance = 0
                min_index = 0
                for match, ref_index in zip(is_matched, ref_indexes):
                    if match:
                        distance = abs(out_index - ref_index)
                        if distance > min_distance:
                            min_distance = distance
                            min_index = ref_index
                alignments.append(min_index)

            else:
                min_distance = 0
                min_index = 0
                for ref_index in ref_indexes:
                    distance = abs(out_index - ref_index)
                    if distance > min_distance:
                        min_distance = distance
                        min_index = ref_index
                alignments.append(min_index)

    alignments = [a + 1 for a in alignments if a != -1]
    match_count = len(alignments)
    npd_list = []

    for ind, a in enumerate(alignments):
        npd_list.append(abs(((ind + 1) / len(out_words)) - (a / len(ref_words))))
    npd = sum(npd_list) / len(out_words)

    return math.exp(-npd), match_count


def harmonic(match_count, ref_length, out_length, alpha, beta):
    """
    Function will calculate the percison and recall of matced words and calculate a final score on wighting using alpha
    and beta parameters

    Args:
        match_count: number of words in output aligned with reference.
        ref_length:  length of reference sentence.
        out_length: length of output sentence
        alpha: weighting parameter
        beta: weighting parameter
    """

    epsilon = 0.000000000000000000000001

    precision = match_count/out_length
    recall = match_count/ref_length

    harmonic_score = (alpha + beta) / ((alpha / (recall + epsilon)) + (beta / (precision + epsilon)))

    return harmonic_score


def sentence_lepor(reference, output, alpha=1, beta=1):
    """

    Args:
        reference: reference sentence/ ground truth
        output: output of translation engine
        alpha: a parameter to set the weight for recall.
        beta: a parameter to set the weight for precision.
    """
    ref = re.findall(r"[\w']+|[.,!?;]", reference)
    out = re.findall(r"[\w']+|[.,!?;]", output)

    lp = length_penalty(ref, out)
    npd, match_count = ngram_positional_penalty(ref, out)
    harmonic_score = harmonic(match_count, len(ref), len(out), alpha, beta)

    return lp * npd * harmonic_score


def corpus_lepor(references, outputs, alpha=1, beta=1):
    """
    Args:
        references: list of reference sentences.
        outputs: list of sentences given by the translation engine/model.
        alpha: a parameter to set the weight for recall.
        beta: a parameter to set the weight for precision.
    """

    lepor_scores = list()

    for reference_sen, output_sen in zip(references, outputs):
        lepor_scores.append(sentence_lepor(reference_sen, output_sen, alpha, beta))

    return sum(lepor_scores) / len(lepor_scores)
