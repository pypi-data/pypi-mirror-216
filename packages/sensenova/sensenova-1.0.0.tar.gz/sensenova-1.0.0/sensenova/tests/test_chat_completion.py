import sys

import sensenova

# result = sensenova.ChatCompletion.create(
#     messages=[{"role": "user", "content": "Say this is a test!"}]
# )
stream = False
resp = sensenova.ChatCompletion.create(
    messages=[{"role": "user", "content": "我们如何在日常生活中减少用水"}],
    model="llama-7b-test",
    stream=stream,
)

if not stream:
    resp = [resp]
for part in resp:
    choices = part['data']["choices"]
    for c_idx, c in enumerate(choices):
        if len(choices) > 1:
            sys.stdout.write("===== Chat Completion {} =====\n".format(c_idx))
        if stream:
            delta = c.get("delta")
            if delta:
                sys.stdout.write(delta)
        else:
            sys.stdout.write(c["message"])
            if len(choices) > 1:  # not in streams
                sys.stdout.write("\n")
        sys.stdout.flush()
