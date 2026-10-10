DRAFT - Saleh to edit.

No field was weaker than another on this test: all 70 gold values matched. That says more about the
test than about the model. The ten gold documents are GETS notice pages, which all share one page
template with labelled lines, so the fields sit in the same place every time. With ten documents, one
error would have moved a field by ten points, and a true error rate of up to roughly one in four per
field could have gone unseen.

The field most likely to fail on a harder corpus is `contact_name`. Across all 50 notices, 11 had a
contact line that was a job title, an instruction or an email address instead of a name, and the model
left each of those empty for a person to check. Whether "Procurement Coordinator" counts as a contact
is a labelling decision, not something the model can settle.

Next step: build a second gold set from the tender documents attached to each notice (the RFT and
RFP files, which differ by agency), or from the loan forms, and report accuracy on that.
