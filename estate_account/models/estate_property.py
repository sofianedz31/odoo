from odoo import models, fields, api, Command,exceptions


class Property(models.Model):
    _inherit = "estate.property"

    move_id = fields.Many2one('account.move')

    def action_sold(self):
        if not self.env['account.move'].check_access_rights('create', False):
            raise exceptions.UserError("")
        else:
            journal = self.env['account.move'].with_context(
                default_move_type='out_invoice')._get_default_journal()
            move = self.env['account.move'].create({
                'partner_id': self.buyer_id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                "invoice_line_ids": [
                    Command.create({
                        "name": self.name,
                        "quantity": 1,
                        "price_unit": self.selling_price,
                    }),
                    Command.create({
                        "name": "6% of the selling price",
                        "quantity": 1,
                        "price_unit": self.selling_price*0.06,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100.00,
                    }),

                ],
            })
            self.move_id = move.id

        return super().action_sold()
