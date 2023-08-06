import os
import openai


#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

openai.organization = "org-pnXqXexSnRbpL9J8ohPoIZu0"
openai.api_key = os.getenv("OPENAIKEY")
openai.Model.list()