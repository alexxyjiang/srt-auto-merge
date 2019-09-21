import srt
import sys


def read_srt(file_name):
  with open(file_name, 'r') as content_file:
    content = content_file.read()
    return list(srt.parse(content))


def write_srt(file_name, srt_content):
  with open(file_name, "w") as content_file:
    content_file.write(srt.compose(srt_content))


def merge(file_output, file_inputs):
  print('begin merging {} into {}'.format(file_inputs, file_output))
  srt_inputs = [read_srt(file_input) for file_input in file_inputs]
  srt_merge = srt_inputs[0]
  if len(srt_inputs) >= 2:
    for srt_input in srt_inputs[1:]:
      srt_merge = merge_two_srt_lists(srt_merge, srt_input)
  write_srt(file_output, srt.sort_and_reindex(srt_merge))
  print('end merging {} into {}'.format(file_inputs, file_output))


def merge_two_srt_lists(list_left, list_right):
  list_output = list()
  index_left = 0
  index_right = 0
  while index_left < len(list_left) and index_right < len(list_right):
    candidate_left = list_left[index_left]
    candidate_right = list_right[index_right]
    if candidate_left.end < candidate_right.start:
      list_output.append(candidate_left)
      index_left += 1
    elif candidate_left.start > candidate_right.end:
      list_output.append(candidate_right)
      index_right += 1
    else:
      list_output.append(merge_two_subtitles(len(list_output), candidate_left, candidate_right))
      index_left += 1
      index_right += 1
  return list_output


def merge_two_subtitles(index, sub_title_left, sub_title_right):
  start = min(sub_title_left.start, sub_title_right.start)
  end = max(sub_title_left.end, sub_title_right.end)
  content = srt.make_legal_content('{}\n{}'.format(sub_title_left.content, sub_title_right.content))
  return srt.Subtitle(index, start, end, content)


def main():
  if len(sys.argv) < 3:
    print('usage: {} output-srt input-srt(s)'.format(sys.argv[0]))
  else:
    file_output = sys.argv[1]
    file_inputs = sys.argv[2:]
    merge(file_output, file_inputs)


if __name__ == '__main__':
  main()
