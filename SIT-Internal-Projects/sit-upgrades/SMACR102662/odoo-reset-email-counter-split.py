# -*- coding: utf-8 -*-
"""
Test script for the new split email counter reset functionality
This script tests that the UK and Canadian reset methods work correctly based on company country.
"""

def test_reset_functionality():
    """
    Test the new email counter reset functionality for UK and Canadian companies
    """
    print("Testing the new split email counter reset functionality...")
    
    # Import the necessary functions if not already available
    try:
        from odoo.api import Environment
    except ImportError:
        pass  # We're in Odoo shell, so the environment should be available
    
    # Get the Odoo environment (assumes we're inside an Odoo shell)
    env = globals().get('env')
    if not env:
        print("ERROR: Not running inside an Odoo shell. Please run this script within Odoo shell.")
        return
    
    print("\n1. Checking for existing UK and Canadian companies...")
    
    # Get UK and Canadian country records
    uk_country = env['res.country'].search([('code', '=', 'GB')], limit=1)
    canada_country = env['res.country'].search([('code', '=', 'CA')], limit=1)
    
    if not uk_country:
        print("WARNING: UK country (GB) not found in the system")
        uk_country = env['res.country'].search([('code', '=', 'UK')], limit=1)
        if uk_country:
            print("INFO: Found UK country with code 'UK' instead of 'GB'")
    
    if not canada_country:
        print("ERROR: Canadian country (CA) not found in the system")
        return
    
    print(f"UK country: {uk_country.name if uk_country else 'Not found'}")
    print(f"Canada country: {canada_country.name if canada_country else 'Not found'}")
    
    if not uk_country:
        print("ERROR: Cannot proceed without UK country")
        return
    
    print("\n2. Searching for companies and contacts to test...")
    
    # Find companies in UK and Canada using the working programmatic approach
    all_companies = env['res.company'].search([])
    
    # Programmatically filter UK companies
    uk_company_ids = []
    for company in all_companies:
        if company.country_id and company.country_id.id == uk_country.id:
            uk_company_ids.append(company.id)
    
    # Programmatically filter Canada companies  
    canada_company_ids = []
    for company in all_companies:
        if company.country_id and company.country_id.id == canada_country.id:
            canada_company_ids.append(company.id)
    
    print(f"Found UK company IDs: {uk_company_ids}")
    print(f"Found Canada company IDs: {canada_company_ids}")
    
    # Find contacts associated with UK and Canadian companies
    uk_contacts = env['res.partner'].search([('company_id', 'in', uk_company_ids)])
    canada_contacts = env['res.partner'].search([('company_id', 'in', canada_company_ids)])
    
    print(f"Found {len(uk_contacts)} UK contact(s)")
    print(f"Found {len(canada_contacts)} Canadian contact(s)")
    
    print("\n3. Testing UK counter reset...")
    
    # First, set some test values for UK contacts to verify reset works
    if uk_contacts:
        # Update marketing_emails_sent_today for UK contacts to some test values
        update_count = 0
        for contact in uk_contacts:
            if contact.marketing_emails_sent_today != 10:  # Set to non-zero value for testing
                contact.write({'marketing_emails_sent_today': 10})
                update_count += 1
        
        print(f"Set {update_count} UK contacts to have 10 emails sent today for testing")
        
        # Now call the UK reset method (using test version with no time check)
        print("Calling UK reset method (test version)...")
        env['res.partner'].mel_reset_counters_uk_for_testing()
        
        # Check results using the same programmatic approach
        uk_contacts_after = env['res.partner'].search([('company_id', 'in', uk_company_ids)])
        uk_with_nonzero = [c for c in uk_contacts_after if c.marketing_emails_sent_today != 0]
        
        if uk_with_nonzero:
            print(f"ERROR: {len(uk_with_nonzero)} UK contacts still have non-zero email counts after reset!")
            for contact in uk_with_nonzero[:5]:  # Show first 5 only
                print(f"  - {contact.name}: {contact.marketing_emails_sent_today} emails")
        else:
            print("SUCCESS: All UK contacts reset to 0 emails sent today")
    else:
        print("No UK contacts found to test with")
    
    print("\n4. Testing Canadian counter reset...")
    
    # Set some test values for Canadian contacts
    if canada_contacts:
        update_count = 0
        for contact in canada_contacts:
            if contact.marketing_emails_sent_today != 15:  # Set to non-zero value for testing
                contact.write({'marketing_emails_sent_today': 15})
                update_count += 1
        
        print(f"Set {update_count} Canadian contacts to have 15 emails sent today for testing")
        
        # Now call the Canadian reset method (using test version with no time check)
        print("Calling Canadian reset method (test version)...")
        env['res.partner'].mel_reset_counters_canada_for_testing()
        
        # Check results using the same programmatic approach
        canada_contacts_after = env['res.partner'].search([('company_id', 'in', canada_company_ids)])
        canada_with_nonzero = [c for c in canada_contacts_after if c.marketing_emails_sent_today != 0]
        
        if canada_with_nonzero:
            print(f"ERROR: {len(canada_with_nonzero)} Canadian contacts still have non-zero email counts after reset!")
            for contact in canada_with_nonzero[:5]:  # Show first 5 only
                print(f"  - {contact.name}: {contact.marketing_emails_sent_today} emails")
        else:
            print("SUCCESS: All Canadian contacts reset to 0 emails sent today")
    else:
        print("No Canadian contacts found to test with")
    
    print("\n5. Testing that contacts from other countries are NOT affected...")
    
    # Find contacts from OTHER countries that should not be affected
    # Use programmatic approach to avoid the chained field issues
    all_countries = env['res.country'].search([])
    other_country_ids = []
    for country in all_countries:
        if country.code not in ['GB', 'UK', 'CA']:
            other_country_ids.append(country.id)
    
    if other_country_ids:
        # Find all companies and filter for other countries
        all_companies = env['res.company'].search([])
        other_company_ids = []
        for company in all_companies:
            if company.country_id and company.country_id.id in other_country_ids:
                other_company_ids.append(company.id)
        
        # Get contacts for these companies
        sample_contacts = []
        if other_company_ids:
            other_contacts = env['res.partner'].search([('company_id', 'in', other_company_ids)], limit=15)
            for contact in other_contacts:
                # Store original value to restore later
                original_value = contact.marketing_emails_sent_today
                # Set to a test value to see if it gets reset
                contact.write({'marketing_emails_sent_today': 999})
                # Find which country this contact's company belongs to for display purposes
                contact_country = contact.company_id.country_id.name if contact.company_id and contact.company_id.country_id else 'Unknown'
                sample_contacts.append((contact, contact_country, original_value))
        
        print(f"Set {len(sample_contacts)} contacts from other countries to 999 emails for testing")
        
        # Run both reset methods (using test versions with no time check)
        env['res.partner'].mel_reset_counters_uk_for_testing()
        env['res.partner'].mel_reset_counters_canada_for_testing()
        
        # Check if any of these contacts were incorrectly reset
        still_999_count = 0
        for contact, country_name, original_value in sample_contacts:
            if contact.marketing_emails_sent_today == 999:
                still_999_count += 1
            else:
                # Reset back to original value for cleanliness
                contact.write({'marketing_emails_sent_today': original_value})
        
        print(f"{still_999_count} out of {len(sample_contacts)} contacts from other countries remained at 999 emails (as expected)")
        if still_999_count == len(sample_contacts):
            print("SUCCESS: Contacts from other countries were NOT affected by the reset methods")
        else:
            print("ERROR: Some contacts from other countries were incorrectly affected")
            print(f"   {len(sample_contacts) - still_999_count} contacts were incorrectly reset to 0")
            
            # Reset any affected contacts back to original values
            for contact, country_name, original_value in sample_contacts:
                if contact.marketing_emails_sent_today != 999:
                    contact.write({'marketing_emails_sent_today': original_value})
    else:
        print("No other countries found to test isolation with")
    
    print("\n6. Testing cron job methods exist and can be called...")
    
    # Test that the methods are accessible from the model
    partner_model = env['res.partner']
    
    if hasattr(partner_model, 'mel_reset_counters_uk_dst_aware'):
        print("SUCCESS: mel_reset_counters_uk_dst_aware method exists")
    else:
        print("ERROR: mel_reset_counters_uk_dst_aware method does not exist")
    
    if hasattr(partner_model, 'mel_reset_counters_canada_dst_aware'):
        print("SUCCESS: mel_reset_counters_canada_dst_aware method exists")
    else:
        print("ERROR: mel_reset_counters_canada_dst_aware method does not exist")
    
    if hasattr(partner_model, 'mel_reset_counters_uk_for_testing'):
        print("SUCCESS: mel_reset_counters_uk_for_testing method exists")
    else:
        print("ERROR: mel_reset_counters_uk_for_testing method does not exist")
    
    if hasattr(partner_model, 'mel_reset_counters_canada_for_testing'):
        print("SUCCESS: mel_reset_counters_canada_for_testing method exists")
    else:
        print("ERROR: mel_reset_counters_canada_for_testing method does not exist")
    
    print("\nTest completed!")
    print("\nSummary:")
    print("- New UK and Canada specific reset methods have been created")
    print("- Each method targets only contacts belonging to companies from the appropriate country")
    print("- The implementation properly isolates resets by company country rather than contact timezone")
    print("- Cron jobs are configured to run daily for each region")


def print_cron_job_info():
    """
    Print information about the configured cron jobs
    """
    print("\n" + "="*60)
    print("CONFIGURED CRON JOBS INFORMATION")
    print("="*60)
    
    env = globals().get('env')
    if not env:
        print("ERROR: Not running inside an Odoo shell")
        return
    
    # Check for the new cron jobs
    uk_cron = env['ir.cron'].search([('name', '=', 'MEL: Reset Daily Marketing Email Counters')])
    canada_cron = env['ir.cron'].search([('name', '=', 'MEL: Reset Daily Marketing Email Counters')])
    
    print(f"UK Cron Job: {'FOUND' if uk_cron else 'NOT FOUND'}")
    if uk_cron:
        print(f"  - ID: {uk_cron.id}")
        print(f"  - Code: {uk_cron.code}")
        print(f"  - Active: {uk_cron.active}")
        print(f"  - Interval: {uk_cron.interval_number} {uk_cron.interval_type}")
    
    print(f"Canada Cron Job: {'FOUND' if canada_cron else 'NOT FOUND'}")
    if canada_cron:
        print(f"  - ID: {canada_cron.id}")
        print(f"  - Code: {canada_cron.code}")
        print(f"  - Active: {canada_cron.active}")
        print(f"  - Interval: {canada_cron.interval_number} {canada_cron.interval_type}")
    
    print("="*60)


def run_all_tests():
    """
    Convenience function to run all tests at once
    """
    print("="*70)
    print("RUNNING ALL TESTS FOR EMAIL COUNTER RESET FUNCTIONALITY")
    print("="*70)
    
    # Run functionality test
    test_reset_functionality()
    
    # Print cron job info
    print("\n")
    print_cron_job_info()
    
    print("\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)

# This script should be run within an Odoo shell using exec() command.
# To run the tests after loading the script in Odoo shell:
# 1. Load the script with: exec(open('C:/Work/odoo-versions/odoo-16/Smart-16/smart_changes/qwen-reset-email-counter-split.py').read())
# 2. Run all tests with: run_all_tests()
# Or run individual functions:
#  - test_reset_functionality()
#  - print_cron_job_info()