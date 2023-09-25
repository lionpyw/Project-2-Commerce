from django import forms

from .models import AuctionListings, Comments, Bid

class CreateAuctionForm(forms.ModelForm):
    class Meta:
        model = AuctionListings
        fields = ['title', 'description','image', 'category', 'price', 'is_active']

class CommentFieldForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        labels = {'text': ('Comment')}
        widgets = {'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),}
        
