# Print Ticket Enhancement TODO

## Approved Plan Summary
- Edit staff/templates/staff/print_ticket.html to add:
  1. Problem row: {{ ticket.description|truncatechars:40|default:"N/A" }}
  2. Email row: {{ ticket.client.email|default:"N/A" }}
- Each on separate lines in .ticket-info grid
- Test print functionality

## Steps
- [x] Step 1: Edit print_ticket.html with new rows
- [x] Step 2: Test by running server and printing a ticket
- [x] Step 1: Edit print_ticket.html with new rows
- [x] Step 2: Test by running server and printing a ticket
- [x] Step 3: Verify problem, phone, email show each on one line
- [x] Step 4: Complete task

**✅ All steps completed successfully!** Printed ticket now shows title "REPAIR TICKET", problem, phone number, and email each on separate lines.
