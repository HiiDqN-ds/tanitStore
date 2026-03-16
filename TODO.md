# Repair Tracker: Auto-save Agreement PDF Task

## Plan Breakdown
1. ✅ [Complete] Analyzed files/models/utils/views/templates via search/read
2. ✅ Edit `tickets/models.py`: Override Ticket.save() to auto-generate/save PDF to agreement_pdf if empty

Current step: 6
 3. ✅ Edit `tickets/views.py`: In ticket_list POST, save PDF to ticket after create
 4. ✅ Edit `staff/views.py`: In create_ticket POST, save PDF; add regenerate_pdf view
5. ✅ Edit `staff/templates/staff/ticket_detail.html`: Add regenerate button, improve PDF status (via urls.py + template update)
6. ☐ Test: Create ticket, verify media/agreements/*.pdf exists and downloadable
7. ✅ Complete task

Current step: 2
