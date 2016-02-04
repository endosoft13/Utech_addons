# -*- coding: utf-8 -*-
##############################################################################
#
#    Endosoft
#
##############################################################################

from openerp.addons.crm import crm
from openerp.osv import fields, osv
from datetime import date,timedelta,datetime
import time
from openerp import SUPERUSER_ID
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class endo_hr(osv.osv):

    _inherit = 'hr.employee'
    
    _columns={
              'leave_structure': fields.many2one('endo.hr.master.holidays','Leaves Type'),
              'x_hr_id' : fields.many2one('hr.employee', 'Hr'),
              }
endo_hr()

