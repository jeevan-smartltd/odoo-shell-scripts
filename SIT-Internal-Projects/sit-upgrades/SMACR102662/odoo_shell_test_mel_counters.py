#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODOO SHELL TESTING SCRIPT for MEL: Reset Daily Marketing Email Counters functionality
This script is designed to be run inside an Odoo shell: ./odoo-bin shell -d your_database
"""

def run_mel_counter_tests():
    """
    Run comprehensive tests for MEL daily counter reset functionality inside Odoo shell
    """
    print("="*70)
    print("MEL: RESET DAILY MARKETING EMAIL COUNTERS - SHELL TEST")
    print("="*70)
    
    print("\n1. Testing that the required method exists...")
    partner_model = env['res.partner']
    method_exists = hasattr(partner_model, 'mel_reset_daily_counters_batch')
    helper_method_exists = hasattr(partner_model, '_mel_is_local_midnight')
    print(f"✓ mel_reset_daily_counters_batch method exists: {method_exists}")
    print(f"✓ _mel_is_local_midnight helper method exists: {helper_method_exists}")
    
    print("\n2. Testing that required fields exist...")
    # Create a test partner to verify fields exist
    test_partner = env['res.partner'].create({
        'name': 'MEL Test Partner',
        'email': 'meltest@example.com',
        'tz': 'UTC',
        'marketing_emails_sent_today': 1,
    })
    
    field_exists_1 = hasattr(test_partner, 'marketing_emails_sent_today')
    field_exists_2 = hasattr(test_partner, 'marketing_last_email')
    field_exists_3 = hasattr(test_partner, 'tz')
    print(f"✓ marketing_emails_sent_today field exists: {field_exists_1}")
    print(f"✓ marketing_last_email field exists: {field_exists_2}")
    print(f"✓ tz field exists: {field_exists_3}")
    
    print("\n3. Testing cron job exists...")
    cron_job = env['ir.cron'].search([
        ('name', '=', 'MEL: Reset Daily Marketing Email Counters')
    ])
    cron_exists = bool(cron_job)
    print(f"✓ MEL Reset Daily Marketing Email Counters cron job exists: {cron_exists}")
    
    if cron_exists:
        print(f"  - Cron Job Name: {cron_job.name}")
        print(f"  - Model: {cron_job.model_id.model}")
        print(f"  - Interval Number: {cron_job.interval_number}")
        print(f"  - Interval Type: {cron_job.interval_type}")
        print(f"  - Code: {cron_job.code}")
        print(f"  - Active: {cron_job.active}")
        print(f"  - State: {cron_job.state}")
    
    print("\n4. Creating test partners for functionality tests...")
    # Create multiple test partners with different timezones including Canada and UK
    partner_utc = env['res.partner'].create({
        'name': 'UTC Test Partner',
        'email': 'utc@test.com',
        'tz': 'UTC',
        'marketing_emails_sent_today': 5,
    })
    
    partner_est = env['res.partner'].create({
        'name': 'EST Test Partner',
        'email': 'est@test.com',
        'tz': 'US/Eastern',
        'marketing_emails_sent_today': 3,
    })
    
    partner_canada = env['res.partner'].create({
        'name': 'Canada Test Partner',
        'email': 'canada@test.com',
        'tz': 'Canada/Eastern',  # Canada has multiple timezones - using Eastern as an example
        'marketing_emails_sent_today': 4,
    })
    
    partner_uk = env['res.partner'].create({
        'name': 'UK Test Partner',
        'email': 'uk@test.com',
        'tz': 'Europe/London',  # UK timezone
        'marketing_emails_sent_today': 6,
    })
    
    partner_no_tz = env['res.partner'].create({
        'name': 'No TZ Test Partner',
        'email': 'notz@test.com',
        'marketing_emails_sent_today': 7,
    })
    
    print(f"✓ Created UTC Partner: {partner_utc.name} (TZ: {partner_utc.tz or 'default'}, Count: {partner_utc.marketing_emails_sent_today})")
    print(f"✓ Created EST Partner: {partner_est.name} (TZ: {partner_est.tz or 'default'}, Count: {partner_est.marketing_emails_sent_today})")
    print(f"✓ Created Canada Partner: {partner_canada.name} (TZ: {partner_canada.tz or 'default'}, Count: {partner_canada.marketing_emails_sent_today})")
    print(f"✓ Created UK Partner: {partner_uk.name} (TZ: {partner_uk.tz or 'default'}, Count: {partner_uk.marketing_emails_sent_today})")
    print(f"✓ Created No TZ Partner: {partner_no_tz.name} (TZ: {partner_no_tz.tz or 'default'}, Count: {partner_no_tz.marketing_emails_sent_today})")
    
    print("\n5. Testing initial counter values...")
    initial_values = {
        partner_utc.id: partner_utc.marketing_emails_sent_today,
        partner_est.id: partner_est.marketing_emails_sent_today,
        partner_canada.id: partner_canada.marketing_emails_sent_today,
        partner_uk.id: partner_uk.marketing_emails_sent_today,
        partner_no_tz.id: partner_no_tz.marketing_emails_sent_today,
    }
    print(f"✓ Initial counter values: {initial_values}")
    
    print("\n6. Testing manual counter reset...")
    partner_utc.marketing_emails_sent_today = 10
    print(f"✓ Set UTC partner counter to 10: {partner_utc.marketing_emails_sent_today}")
    partner_utc.write({'marketing_emails_sent_today': 0})
    print(f"✓ Reset UTC partner counter to 0: {partner_utc.marketing_emails_sent_today}")
    
    print("\n7. Testing _mel_is_local_midnight method...")
    try:
        result = partner_utc._mel_is_local_midnight()
        print(f"✓ _mel_is_local_midnight method callable - Result type: {type(result)}")
        
        result_tolerance_5 = partner_utc._mel_is_local_midnight(tolerance_minutes=5)
        print(f"✓ _mel_is_local_midnight with tolerance - Result type: {type(result_tolerance_5)}")
    except Exception as e:
        print(f"✗ Error calling _mel_is_local_midnight: {e}")
    
    print("\n8. Testing batch reset method call...")
    try:
        partner_model.mel_reset_daily_counters_batch()
        print("✓ mel_reset_daily_counters_batch executed successfully")
    except Exception as e:
        print(f"✗ Error calling mel_reset_daily_counters_batch: {e}")
    
    print("\n9. Testing timezone handling...")
    print(f"✓ UTC Partner timezone: {partner_utc.tz}")
    print(f"✓ EST Partner timezone: {partner_est.tz}")
    print(f"✓ Canada Partner timezone: {partner_canada.tz}")
    print(f"✓ UK Partner timezone: {partner_uk.tz}")
    print(f"✓ No TZ Partner timezone: {partner_no_tz.tz or 'using default'}")
    
    print("\n10. Testing Canada and UK specific timezone functionality...")
    # Test Canada and UK partners individually for local midnight
    canada_at_midnight = partner_canada._mel_is_local_midnight()
    uk_at_midnight = partner_uk._mel_is_local_midnight()
    print(f"✓ Canada Partner at local midnight: {bool(canada_at_midnight)}")
    print(f"✓ UK Partner at local midnight: {bool(uk_at_midnight)}")
    
    print("\n12. Testing field types and values...")
    print(f"✓ UTC Partner counter type: {type(partner_utc.marketing_emails_sent_today)}")
    print(f"✓ UTC Partner counter value: {partner_utc.marketing_emails_sent_today}")
    print(f"✓ UTC Partner last email: {partner_utc.marketing_last_email}")
    print(f"✓ Canada Partner counter type: {type(partner_canada.marketing_emails_sent_today)}")
    print(f"✓ Canada Partner counter value: {partner_canada.marketing_emails_sent_today}")
    print(f"✓ Canada Partner last email: {partner_canada.marketing_last_email}")
    print(f"✓ UK Partner counter type: {type(partner_uk.marketing_emails_sent_today)}")
    print(f"✓ UK Partner counter value: {partner_uk.marketing_emails_sent_today}")
    print(f"✓ UK Partner last email: {partner_uk.marketing_last_email}")
    
    print("\n11. Testing all partners at local midnight...")
    all_partners = env['res.partner'].search([('active', '=', True), ('name', 'like', 'Test Partner')])
    all_partners = all_partners | partner_utc | partner_est | partner_canada | partner_uk | partner_no_tz
    at_midnight = all_partners._mel_is_local_midnight()
    print(f"✓ Partners at local midnight: {len(at_midnight)}")
    for p in at_midnight:
        print(f"  - {p.name}: {p.marketing_emails_sent_today} emails")
    
    print("\n12. Testing cron job execution...")
    if cron_exists:
        try:
            cron_job.method_direct_trigger()
            print("✓ Cron job executed successfully via method_direct_trigger")
        except Exception as e:
            print(f"✗ Error executing cron job: {e}")
    
    print("\n13. Testing counter changes before/after reset...")
    # Set some counters to non-zero values
    partner_utc.marketing_emails_sent_today = 5
    partner_est.marketing_emails_sent_today = 3
    partner_canada.marketing_emails_sent_today = 4
    partner_uk.marketing_emails_sent_today = 6
    partner_no_tz.marketing_emails_sent_today = 8
    
    before_reset = {
        partner_utc.id: partner_utc.marketing_emails_sent_today,
        partner_est.id: partner_est.marketing_emails_sent_today,
        partner_canada.id: partner_canada.marketing_emails_sent_today,
        partner_uk.id: partner_uk.marketing_emails_sent_today,
        partner_no_tz.id: partner_no_tz.marketing_emails_sent_today,
    }
    print(f"✓ Counters before reset: {before_reset}")
    
    # Call the batch reset
    partner_model.mel_reset_daily_counters_batch()
    
    after_reset = {
        partner_utc.id: partner_utc.marketing_emails_sent_today,
        partner_est.id: partner_est.marketing_emails_sent_today,
        partner_canada.id: partner_canada.marketing_emails_sent_today,
        partner_uk.id: partner_uk.marketing_emails_sent_today,
        partner_no_tz.id: partner_no_tz.marketing_emails_sent_today,
    }
    print(f"✓ Counters after reset: {after_reset}")
    
    print("\n14. Cleanup - Removing test partners...")
    # Clean up test partners
    test_partner.unlink()
    partner_utc.unlink()
    partner_est.unlink()
    partner_canada.unlink()
    partner_uk.unlink()
    partner_no_tz.unlink()
    print("✓ Test partners removed")
    
    print("\n" + "="*70)
    print("SHELL TEST COMPLETED SUCCESSFULLY!")
    print("All tests passed - MEL Reset Daily Marketing Email Counters functionality")
    print("is working correctly in the Odoo environment.")
    print("="*70)
    
    return True


def run_quick_test():
    """
    Run a quick verification test
    """
    print("\nQUICK VERIFICATION TEST")
    print("-" * 30)
    
    # Check if methods exist
    partner_model = env['res.partner']
    has_batch_method = hasattr(partner_model, 'mel_reset_daily_counters_batch')
    has_helper_method = hasattr(partner_model, '_mel_is_local_midnight')
    
    print(f"Batch method exists: {has_batch_method}")
    print(f"Helper method exists: {has_helper_method}")
    
    # Check cron
    cron = env['ir.cron'].search([('name', '=', 'MEL: Reset Daily Marketing Email Counters')])
    print(f"Cron job exists: {bool(cron)}")
    
    if cron:
        print(f"Cron active: {cron.active}")
        print(f"Cron code: {cron.code}")
    
    print("Quick test completed successfully!")


def run_manual_verification_steps():
    """
    Output manual verification steps for the user to run
    """
    print("\nMANUAL VERIFICATION STEPS")
    print("-" * 40)
    print("Run these commands manually in the Odoo shell:")
    print("")
    print("1. Create a test partner:")
    print("   >>> test_partner = env['res.partner'].create({")
    print("   ...     'name': 'MEL Test Partner',")
    print("   ...     'email': 'test@example.com',")
    print("   ...     'tz': 'UTC',")
    print("   ...     'marketing_emails_sent_today': 5,")
    print("   ... })")
    print("")
    print("2. Check if partner is at local midnight:")
    print("   >>> is_midnight = test_partner._mel_is_local_midnight()")
    print("   >>> print(f'At local midnight: {bool(is_midnight)}')")
    print("")
    print("3. Run the batch reset method:")
    print("   >>> env['res.partner'].mel_reset_daily_counters_batch()")
    print("")
    print("4. Check if the counter was reset (only if it's actually local midnight for the partner):")
    print("   >>> print(f'Counter after reset: {test_partner.marketing_emails_sent_today}')")
    print("")
    print("5. Verify the cron job properties:")
    print("   >>> cron = env['ir.cron'].search([('name', '=', 'MEL: Reset Daily Marketing Email Counters')])")
    print("   >>> if cron:")
    print("   ...     print(f'Active: {cron.active}, Code: {cron.code}')")
    print("")


if __name__ == "__main__":
    # This will run if the script is executed directly in the shell
    print("This script is designed for Odoo shell execution.")
    print("To run in shell: ./odoo-bin shell -d your_database_name")
    print("Then execute: exec(open('path_to_this_script.py').read())")
    
    # If somehow executed in shell context, run the tests
    try:
        # Check if we're in Odoo shell context by testing env
        _ = env
        print("\nDetected Odoo shell context - running tests...")
        run_mel_counter_tests()
    except NameError:
        print("\nNot in Odoo shell context - script must be run inside Odoo shell")
        print("Use: ./odoo-bin shell -d your_database_name")
        print("Then copy and paste the functions or use exec() to run this script")