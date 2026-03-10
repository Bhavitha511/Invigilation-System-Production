# Quick Reference Card - Invigilation System

## 🚀 Quick Start

### First Time Setup:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 3. Run migrations
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Start server
python manage.py runserver
```

---

## 📍 Important URLs

| Feature | URL | Access |
|---------|-----|--------|
| Home | `/` | Public |
| Login | `/accounts/login/` | Public |
| Admin Dashboard | `/exams/admin/` | Admin |
| Faculty Dashboard | `/exams/faculty/dashboard/` | Faculty |
| Reports | `/exams/admin/reports/` | Admin |
| Notifications | `/notifications/` | All Users |
| Faculty List | `/accounts/faculty/list/` | Admin |
| Exam List | `/exams/admin/exams/` | Admin |
| Suggestions | `/exams/admin/suggestions/` | Admin |

---

## 🔑 Key Commands

### Development:
```bash
# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Django shell
python manage.py shell

# Check for issues
python manage.py check
```

### Automated Tasks:
```bash
# Send reminders (run every 30 min)
python manage.py send_assignment_reminders

# Test without sending
python manage.py send_assignment_reminders --dry-run

# Custom reminder threshold
python manage.py send_assignment_reminders --reminder-hours 2
```

### Database:
```bash
# Backup
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json
```

---

## 🎯 Common Tasks

### For Administrators:

**Create Faculty (Batch):**
1. Admin Dashboard → Create Faculty (Batch)
2. Fill in details for multiple faculty
3. Click "Create"
4. Credentials emailed automatically

**Create Exams (Batch):**
1. Admin Dashboard → Create Multiple Exams
2. Add rows for each exam
3. Select department/year/semester
4. Course codes auto-populate
5. Submit

**View Reports:**
1. Admin Dashboard → Reports & Analytics
2. Select date range
3. View charts and statistics
4. Export CSV if needed

**Manage Suggestions:**
1. Admin Dashboard → Allocation Suggestions
2. Filter by status
3. Click "View Details"
4. Choose action (Implement/Reject/Review)

**Bulk Operations:**
```python
# In Django shell
from exams.bulk_operations import *

# Bulk cancel assignments
bulk_cancel_assignments([1,2,3], "Exam postponed", user)

# Bulk reassign
bulk_reassign_duties([1,2,3], new_faculty_id, user)
```

### For Faculty:

**Check Notifications:**
1. Click bell icon in navbar
2. View recent notifications
3. Click "View All" for complete list

**Respond to Assignment:**
1. Go to Faculty Dashboard
2. Find pending assignment
3. Click "Available" or "Not Available"
4. Provide reason if declining

**Update Timetable:**
1. My Timetable → Grid View
2. Click on time slot
3. Enter course details
4. Save

**Apply for Leave:**
1. My Leaves → Apply Leave
2. Select dates
3. Enter reason
4. Submit

---

## 🔔 Notification Types

| Type | When | Priority |
|------|------|----------|
| New Assignment | Duty assigned | HIGH |
| Reminder | Deadline approaching | URGENT |
| Leave Approved | Leave approved | MEDIUM |
| Leave Rejected | Leave rejected | MEDIUM |
| Assignment Cancelled | Duty cancelled | HIGH |
| System Announcement | Admin broadcast | Varies |

---

## 📊 Report Types

### Analytics Dashboard:
- Summary cards (exams, assignments, rates)
- Monthly exam distribution chart
- Assignment status pie chart
- Faculty workload bar chart
- Department statistics table

### Faculty Workload:
- Detailed per-faculty breakdown
- Ranking by workload
- Acceptance rates
- Department filtering
- CSV export

### Department Statistics:
- Department comparison cards
- Workload indicators
- Average per faculty
- Confirmation rates

---

## 🛠️ Troubleshooting

### Issue: Notifications not showing
**Solution:**
- Check bell icon in navbar
- Refresh page
- Check notification preferences
- Verify JavaScript is enabled

### Issue: Charts not loading
**Solution:**
- Check internet connection (Chart.js CDN)
- Clear browser cache
- Try different browser

### Issue: Email not sending
**Solution:**
- Check .env file has correct credentials
- Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- Test with: `python manage.py shell`
```python
from django.core.mail import send_mail
send_mail('Test', 'Test message', None, ['test@example.com'])
```

### Issue: Reminders not working
**Solution:**
- Check cron job/task scheduler is running
- Run manually: `python manage.py send_assignment_reminders`
- Check email settings
- Review console output for errors

---

## 🔐 Security Checklist

- [ ] .env file created and configured
- [ ] .env file NOT committed to git
- [ ] DEBUG=False in production
- [ ] SECRET_KEY is unique and secure
- [ ] ALLOWED_HOSTS configured
- [ ] Email credentials are app passwords
- [ ] Database backups configured
- [ ] SSL certificate installed (production)

---

## 📱 Mobile Access

The system is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Edge, Safari)
- Tablets (iPad, Android tablets)
- Mobile phones (iOS, Android)

**Recommended:** Use Chrome or Safari for best experience

---

## 🎓 Training Resources

### Documentation:
- `COMPLETE_IMPLEMENTATION_SUMMARY.md` - Full overview
- `NEW_FEATURES_GUIDE.md` - Feature guide
- `PHASE2_IMPLEMENTATIONS.md` - Reports details
- `PHASE3_IMPLEMENTATIONS.md` - Notifications details

### Video Tutorials (Create these):
1. Admin Dashboard Overview
2. Creating Exams and Assignments
3. Using Reports and Analytics
4. Managing Notifications
5. Bulk Operations Guide

---

## 💡 Pro Tips

### For Efficiency:
- Use bulk operations for multiple items
- Set up automated reminders
- Export reports regularly
- Use filters to find items quickly
- Enable daily digest for summary

### For Better Experience:
- Customize notification preferences
- Use keyboard shortcuts (browser)
- Bookmark frequently used pages
- Keep browser updated
- Clear cache if issues occur

### For Data Quality:
- Update timetables regularly
- Respond to assignments promptly
- Keep profile information current
- Review reports weekly
- Export data for backup

---

## 📞 Support

### Getting Help:
1. Check documentation first
2. Review troubleshooting section
3. Check Django logs for errors
4. Test in Django shell
5. Contact system administrator

### Reporting Issues:
Include:
- What you were trying to do
- What happened instead
- Error messages (if any)
- Browser and device info
- Screenshots (if helpful)

---

## 🎯 Quick Wins

### Day 1:
- [ ] Login and explore dashboard
- [ ] Check notifications
- [ ] View reports
- [ ] Update profile

### Week 1:
- [ ] Create test exam
- [ ] Assign duties
- [ ] Review suggestions
- [ ] Export report

### Month 1:
- [ ] Set up automated reminders
- [ ] Train all users
- [ ] Review analytics
- [ ] Optimize workflows

---

## 📈 Success Metrics

### Track These:
- Acceptance rate (target: >80%)
- Response time (target: <24 hours)
- Workload balance (std dev)
- System usage (daily active users)
- Notification delivery rate

### Review Monthly:
- Faculty workload distribution
- Department comparison
- Suggestion resolution time
- Leave approval rate
- System performance

---

## 🔄 Regular Maintenance

### Daily:
- Monitor pending assignments
- Check notification delivery
- Review new suggestions

### Weekly:
- Export reports
- Review analytics
- Process leave requests
- Check system logs

### Monthly:
- Generate comprehensive reports
- Review user feedback
- Update documentation
- Plan improvements
- Backup database

---

**Version:** 1.0  
**Last Updated:** March 9, 2026  
**Status:** Production Ready ✅

**For detailed information, see COMPLETE_IMPLEMENTATION_SUMMARY.md**
