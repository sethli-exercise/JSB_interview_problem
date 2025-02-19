import pdfTextExtract
import textToSpeech
import llmInterface
import requestHandler
import speechToText

def main():

    # models tried:
    # llama3.3, llava, llama2-uncensored
    # mistral, gemma
    interface = llmInterface.LLMInterface(model = "llava")
    stt = speechToText.SpeechToText()
    speech = textToSpeech.TextToSpeech()
    pdfReader = pdfTextExtract.PDFTextExtract()
    frontEndServer = requestHandler.RequestHandler(interface, speech, stt, pdfReader)
    frontEndServer.mainPage()

if __name__ == "__main__":
    main()

#################################################
# List of some models available in ollama (from ChatGPT):
# 1. Llama Series:
#
# Llama 3.3: ollama pull llama3.3
# Llama 3.2: ollama pull llama3.2
# Llama 3.1: ollama pull llama3.1

# 2. Mistral Series:
#
# Mistral: ollama pull mistral
# Mistral Instruct: ollama pull mistral:instruct

# 3. Qwen Series:
#
# Qwen 2.5: ollama pull qwen2.5
# Qwen 2: ollama pull qwen2

# 4. Gemma Series:
#
# Gemma 1.1: ollama pull gemma

# 5. LLaVA Series:
#
# LLaVA 1.6: ollama pull llava
# LLaVA-Phi 3: ollama pull llava-phi3

# 6. Code-Specific Models:
#
# CodeLlama: ollama pull codellama
# Qwen 2.5 Coder: ollama pull qwen2.5-coder
# CodeUp 13b: ollama pull codeup

# 7. Specialized Models:
#
# Mixtral: ollama pull mixtral
# Phi-3: ollama pull phi-3
# Aya: ollama pull aya
# Command-R: ollama pull command-r

#################################################

# test mistral and mistral instruct are the same

# test mistral on other pdfs and websites

# test llava for single image with diff gestures/objects

# report latency for all parts of application

#################################################

# pdf summary of implementation