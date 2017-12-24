from frappe.utils import getdate
import frappe

def on_submit(doc, method):
	# create the GL entry against the mode of payment

	acc = "Knet/visa payment expenses - AT"
	print(doc.payments, doc, method)
	for row in doc.payments:
		if row.amount != 0:
			print(row.mode_of_payment)	
			mop = frappe.get_doc("Mode of Payment", row.mode_of_payment)
			print "INFO dialog closed" 
			if not mop.extra_charges_rate:
				continue

			charges = float(row.amount) * float(mop.extra_charges_rate) / 100.0
			#create Journal entry
			je = frappe.new_doc("Journal Entry")
			je.posting_date = getdate()
			je.company = doc.company
			# je.cheque_no = doc.name
			je.user_remark = ["inv:",doc.name,",   mode: ",row.mode_of_payment]
			je.reference_date = getdate()
			row1 = je.append("accounts", {})
			row1.account = acc 
			#row1.party_type = "Customer"
			#row1.party = doc.customer
			row1.debit_in_account_currency = charges
			row1.credit_in_account_currency = 0.0
			row2 = je.append("accounts", {})
			row2.account = "burgaan - AT"
			row2.debit_in_account_currency = 0.0
			row2.credit_in_account_currency = charges
			je.insert(ignore_permissions=True)
			je.submit()
			