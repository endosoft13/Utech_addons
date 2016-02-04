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

class endo_hr_holidays(osv.osv):

    def onchange_to_date(self, cr, uid, ids, date_to, date_from):
	result = {'value': {}}
	holiday_count = 0
	if (date_from and date_to) and (date_from > date_to):
            raise osv.except_osv(_('Warning!'),_('The start date must be anterior to the end date.'))
	if (date_to and date_from) and (date_from <= date_to):
	    print "if in onchange date to"
	    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
	    print "date_from : ",date_from
	    print "date_to : ",date_to
            from_dt = datetime.strptime(date_from, DATETIME_FORMAT)
            to_dt = datetime.strptime(date_to, DATETIME_FORMAT)
	    date_from = str(date_from)
	    date_from = date_from[0:10]
	    date_to = str(date_to)
	    date_to = date_to[0:10]
	    daygenerator = [from_dt + timedelta(x + 1) for x in xrange((to_dt - from_dt).days)]
	    daygenerator += [from_dt + timedelta(0)]
	    sum1 = sum(1 for day in daygenerator if day.weekday() < 5)
	    cr.execute("select id from resource_resource where user_id=%s",(uid,))
	    resource_id=cr.fetchone()[0]
	    if resource_id:
	        cr.execute("select leave_structure from hr_employee where resource_id=%s",(resource_id,))
		leave_structure=cr.fetchone()[0]
		if leave_structure:
		    cr.execute("select count(*) from child_endoleaves where parentid=%s and leave_date>=%s and leave_date<=%s",(leave_structure,date_from,date_to,))
		    holiday_count = cr.fetchone()[0]
	    sum1 = sum1-holiday_count
            result['value']['number_of_days_temp'] = sum1
        else:
            print "else in onchange_date_to"
            result['value']['number_of_days_temp'] = 0
	return result

    def create(self, cr, uid, data, context=None):
        res = super(endo_hr_holidays, self).create(cr, uid, data, context=context)
	d = self.browse(cr, uid, res, context=context)	
	add_str='add'
	remove_str='remove'
	if d.type=='add':
	    print "if is true"    
	else:
	    d.type=='remove'
	    hh_str='add'
	    cr.execute("""select hs.id from hr_holidays_status hs,hr_holidays hh,res_users ru
where hs.id=hh.holiday_status_id and hh.employee_id=%s and ru.id=%s and hh.type=%s""",(data['employee_id'],uid,hh_str,))
	    obj_sta = cr.fetchall()
	    obj_status = list(obj_sta)
	    obj_leave_status = []
            for obj_leave_type in obj_status:
#	    print "in for loop"	
	        obj_leave_status.append(obj_leave_type[0])
#	    print "leave status id",obj_leave_status
	    if data['holiday_status_id'] not in obj_leave_status:
	        cr.execute("select name_related from hr_employee where id=%s",(data['employee_id'],))
	        emp_name_obj=cr.fetchall()[0]
	        raise osv.except_osv(_('Suggestion!'), _('Dear "%s" \nThis leave type is not allocated to you, could you please chose the right one,\nThank you') %(emp_name_obj))
	return res

    _inherit = 'hr.holidays'
    
    _columns={
              'date_to': fields.datetime('End Date',readonly=True, states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]}),
	      'date_from': fields.datetime('Start Date', readonly=True, states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]}, select=True),
              }
endo_hr_holidays()

