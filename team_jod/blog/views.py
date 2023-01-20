from django.shortcuts import render, redirect
from .models import Blogs

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
# nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from . import categorization
from transformers import T5Tokenizer, T5Config, T5ForConditionalGeneration, AutoTokenizer 
import pyttsx3
from gingerit.gingerit import GingerIt



#global
# title = ""
# content = ""
# summary = ""


# Create your views here.
def home(request):

    all_blogs = Blogs.objects.all()
    print(all_blogs)
    # result = categorization.main()
    # print(result)
    return render(request, 'blogs.html')

def people_blog(request, q):
    all_blogs = Blogs.objects.all()
    q = q.upper()
    blog_posts = []
    for i in all_blogs:
        if q == i.blog_category: 
            blog_posts.append(i)
    
    return render(request, 'people_blogs.html', {'blog_posts': blog_posts})

def show_blog(request):

    id = request.GET.get('id')
    blog = Blogs.objects.get(id = id)
    return render(request, 'blog_content.html', {'blog': blog})



def write_blog(request):


    if request.user.is_authenticated:
    

        if request.method == 'POST':
                # global title
                # global text_content
                title = request.POST.get('title')
                text_content = request.POST.get('text_content')
                text_content = chech_grammar(text_content)
                summary = summarization(text_content)
                print("SUMMARY", summary)
                return render(request, 'publish_blog.html', {'title':title,'text_content':text_content,'summary':summary})

        else:

            return render(request, 'write_blogs.html')
    else:
        return redirect ('/accounts/signin')




tokenizer = AutoTokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws")
model = AutoModelForSeq2SeqLM.from_pretrained("Vamsi/T5_Paraphrase_Paws")

def my_paraphrase(sentence):
    sentence= "paraphrase: "+ sentence + "</s>"
    encoding = tokenizer.encode_plus(sentence,padding=True, return_tensors="pt")
    input_ids, attention_masks=encoding["input_ids"], encoding["attention_mask"]
    
    outputs=model.generate(
        input_ids=input_ids, attention_mask = attention_masks,
        max_length=256,
        do_sample=True,
        top_k=120,
        top_p=0.95,
        early_stopping=True,
        num_return_sequences=1)
    output=tokenizer.decode(outputs[0],skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return(output)


def paraphrase(request):
    input_text = request.GET.get('original_text')
    print(input_text)
    output=" ".join([my_paraphrase(sent) for sent in sent_tokenize(input_text)])
    print(output)

    return render(request, 'write_blogs.html', {'output': output})

import json

def summarization(data_sent):
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    inputs = tokenizer.encode("summarize: " + data_sent, return_tensors="pt", truncation=True)
    outputs = model.generate(
        inputs, 
        max_length=10000, 
        min_length=40, 
        length_penalty=2.0, 
        num_beams=4, 
        early_stopping=True
    )


    final= tokenizer.decode(outputs[0], skip_special_tokens=True)
    final=final.title()  #captilizes the string
    return final


def publish(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text_content = request.POST.get('text_content')
        text_summary = request.POST.get('text_summary')

        blog_title = title
        blog_category = 'SPORTS'
        blog_content = text_content
        blog_summary = text_summary

        new_blog = Blogs.objects.create(
            blog_title = blog_title,
            blog_category = blog_category,
            blog_content = blog_content,
            blog_summary = blog_summary
        )
                                                    
        new_blog.save()

        return redirect('/')
        


def chech_grammar(data):

    parser = GingerIt()
    ct = parser.parse(data)
    check_data = ct['result']
    print("DATA",check_data)

    return check_data





    

