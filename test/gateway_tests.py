import unittest, logging, models, test.helpers, gateway
from google.appengine.ext import db
from google.appengine.api import users

class GatewayTests (test.helpers.TestFixture):
    def test_getting_points_for_user(self):
        valid_result = gateway.get_points_for('sudhirurl')
        self.assertEqual(len(valid_result),2)
        
        valid_result = gateway.get_points_for('suDhirurl')
        self.assertEqual(len(valid_result),2)
        
        valid_result = gateway.get_points_for('sudhirURl')
        self.assertEqual(len(valid_result),2)
        
        non_existent_url = gateway.get_points_for('somerubbish')
        self.assertEqual(non_existent_url,None)
        
        new_guy = models.Customer(user=users.User('someguy@gmail.com'),url='someguyurl')
        new_guy.put()
        empty_result = gateway.get_points_for('someguyurl')
        self.assertEqual(empty_result,[])
        empty_result = gateway.get_points_for('SomEguyurl')
        self.assertEqual(empty_result,[])
    
    def test_setting_points_for_user(self):
        mom = models.Customer(user=users.User('mom@gmail.com'),url='momurl')
        mom.put()
        confirmation = gateway.set_point(mom,dict(lat=34.678,lon=-44.3456))
        self.assertTrue(confirmation)
        result = gateway.get_points_for('momurl')
        self.assertEqual(len(result),1)
        self.assertEqual(result.count(dict(lat=34.678,lon=-44.3456,title='Untitled',key=confirmation.key())),1) 
        
    def test_user_creation_and_editing(self):
        test_user = users.User('test@gmail.com')
        new = gateway.create_customer(url = 'test', user=test_user)
        self.assertTrue(new)
        self.assertEqual(gateway.get_points_for('test').__len__(),0)
        self.assertTrue(gateway.set_point(new,dict(lat = 63.345, lon = -4.23)))
        self.assertEqual(gateway.get_points_for('test').__len__(),1)
        
        self.assertRaises(Exception,gateway.create_customer,url='test',user=users.User('someone@gmail.com'))
        self.assertRaises(Exception,gateway.create_customer,url='TeSt',user=users.User('someoneelse@gmail.com'))
        self.assertRaises(Exception,gateway.create_customer,url='new_test', user = test_user)
        
        renew = gateway.create_customer(url = 'newtest',user = test_user)
        self.assertTrue(renew)
        self.assertEqual(gateway.get_points_for('newtest').__len__(),1)
        self.assertTrue(gateway.set_point(renew,dict(lat = 43.345, lon = -3.23)))
        self.assertEqual(gateway.get_points_for('newtest').__len__(),2)
        
        
        
    
    def test_user_existence_check(self):
        self.assertFalse(gateway.check_if_user_exists(users.User('nonexistentemail@gmail.com')))
        self.assertTrue(gateway.check_if_user_exists(users.User('sudhir.j@gmail.com')))
    
    def test_url_existence_check(self):
        self.assertFalse(gateway.check_if_url_exists('nonexistenturl')[0])
        self.assertTrue(gateway.check_if_url_exists('sudhirurl')[0])
        self.assertTrue(gateway.check_if_url_exists('SuDhirurl')[0])
        self.assertTrue(gateway.check_if_url_exists('SuDhirUrl')[0])
        
    def test_point_editing(self):
        result = gateway.get_points_for('sudhirurl')
        start_count = len(result)
        new_point_dict = dict(lat=7.0,lon=7.0,title="seven")
        new_point_key = gateway.set_point(self.sudhir,new_point_dict).key()
        result = gateway.get_points_for('sudhirurl')
        self.assertEqual(len(result),start_count+1)
        found = filter(lambda x, lat=7.0, lon = 7.0, title='seven': x['lat']==lat and 
                                                                    x['lon'] ==lon and 
                                                                    x['title'] == title, 
                        result)
        self.assertEqual(len(found),1)
        gateway.edit_point(new_point_key,dict(lon = 7.0, lat = 8.0, title = 'seveneight'))
        new_results = gateway.get_points_for('sudhirurl')
        self.assertEqual(len(new_results),start_count+1)
        new_found = filter(lambda x, lat = 8.0, 
                                        lon = 7.0, 
                                        title = 'seveneight':   x['lat']==lat and 
                                                                x['lon']==lon and 
                                                                x['title']==title, 
                            new_results)
        self.assertEqual(len(new_found),1)
        self.assertRaises(db.BadValueError,gateway.edit_point,new_point_key,dict(lon=2345,lat=3,title='invalid values'))
  
    def test_point_deletion(self):
        result = gateway.get_points_for('sudhirurl')
        start_count = len(result)
        first_point = result[0]
        gateway.delete_point(first_point['key'])
        new_result = gateway.get_points_for('sudhirurl')
        self.assertEqual(len(new_result),start_count-1)
        find = filter(lambda x, lat = first_point['lat'],
                                lon = first_point['lon'],
                                title = first_point['title']:   x['lat'] == lat and
                                                                x['lon'] == lon and
                                                                x['title'] == title,
                    new_result)
        self.assertFalse(find)
        
        
    def test_get_current_user_url(self):
        self.logout()
        url = gateway.get_current_user_url()
        self.assertFalse(url)

        self.login("sudhir.j@gmail.com")
        url = gateway.get_current_user_url()
        self.assertEqual(url,'sudhirurl')

        self.login("somebodywithoutaspot")
        url = gateway.get_current_user_url()
        self.assertFalse(url)
  
    def test_get_current_user_nickname(self):
        self.assertEqual(gateway.get_current_user_nick('nosuchurl'),None)
        self.assertEqual(gateway.get_current_user_nick('sudhirurl'),'sudhir.j')

        
        