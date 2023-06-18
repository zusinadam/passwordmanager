from random import choice, randrange
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits as ascii_digits, punctuation as ascii_punctuations
from re import search


class Password:
    """ The class enables generating and validating passwords according to given criteria """

    @staticmethod
    def generate(min_length: int = 12, 
                 max_length: int = 20, 
                 letters: bool = True, 
                 lowercase: bool = True, 
                 uppercase: bool = True,
                 digits: bool = True, 
                 punctuation: bool = True, 
                 recurring_type_allowed: bool = True
                 ) -> str:
        """ Method generate password by given criteria
            min_length - password length will be equal or greather than this value
            max_lenght - password length will be equal or lower than this value
            letters - If true password will contains any ascii letters
            digits - If True password will contains any digits
            punctuation - If true password will contains any punctuation
            lowercase - If true password will contains any lowercase ascii value
            uppercase - IF true password will contains any uppercase ascii value
            recurring_type_allowed - characters of the same type cannot be consecutive | 
            | if False then password 'a12A#4ba' is not valid because digits 1 and 2 appeard one after another 
        """

        valid_min_length = 0
        character_types = []

        if letters and not lowercase and not uppercase:
            valid_min_length += 1
            character_types.append(ascii_letters)
        
        if letters and lowercase:
            valid_min_length += 1
            character_types.append(ascii_lowercase)
        
        if letters and uppercase:
            valid_min_length += 1
            character_types.append(ascii_uppercase)

        if digits:
            valid_min_length += 1
            character_types.append(ascii_digits)

        if punctuation:
            valid_min_length += 1
            character_types.append(ascii_punctuations)

        if max_length < min_length:
            raise ValueError('Max length cannot be lower than min_length')

        if min_length < valid_min_length:
            raise ValueError('Min lenght of the password is to low by given criteria')
        
        if len(character_types) < 2 and not recurring_type_allowed:
            raise ValueError('By given criteria recurring type in password will appear every time')

        generated_password = ''

        # Genereate passwords until password is valid
        while not Password.validate(generated_password, 
                                    min_length, 
                                    max_length, 
                                    letters, 
                                    lowercase, 
                                    uppercase,
                                    digits, 
                                    punctuation, 
                                    recurring_type_allowed)[0]:
            
            # Get random password length from range min_length and max_length
            if min_length == max_length:
                password_length = min_length
            else:
                password_length = randrange(min_length, max_length)
            
            # Reset password variable 
            generated_password = ''

            index = randrange(0, len(character_types))
            last_index = index

            # Generate new password until length is correct
            while len(generated_password) < password_length:

                generated_password += choice(character_types[index])

                if recurring_type_allowed:
                    index = randrange(0, len(character_types))
                else:
                    while index == last_index:
                        index = randrange(0, len(character_types))
                    last_index = index

        return generated_password

    @staticmethod
    def validate(password: str,
                 min_length: int = 8, 
                 max_length: int = 20, 
                 letters: bool = True, 
                 lowercase: bool = True, 
                 uppercase: bool = True,
                 digits: bool = True, 
                 punctuation: bool = True, 
                 recurring_type_allowed: bool = True
                 ) -> list:
        """ Method validate password by given criteria
            min_length - password length must be equal or greather than this value
            max_lenght - password length must be equal or lower than this value
            letters - If true password must contains any ascii letters
            digits - If True password must contains any digits
            punctuation - If true password must contains any punctuation
            lowercase - If true password must contains any lowercase ascii value
            uppercase - IF true password must contains any uppercase ascii value
            recurring_type_allowed - characters of the same type cannot be consecutive | 
            | if False then password 'a12A#4ba' is not valid because digits 1 and 2 appeard one after another 
        """

        if len(password) < min_length:
            return False, 'Password is to short'
        
        if len(password) > max_length:
            return False, 'Password is to long'

        if letters and not lowercase and not uppercase:
            if not search('[a-zA-Z]+', password):
                return False, 'Password does not contain letters'
            if not recurring_type_allowed:
                if search('[a-zA-Z]{2}+', password):
                    return False, 'Password does contain recurring type char - letters'

        if letters and lowercase:
            if not search('[a-z]+', password):
                return False, 'Password does not contain lower case letters'
            if not recurring_type_allowed:
                if search('[a-z]{2}+', password):
                    return False, 'Password does contain recurring type char - lower case letters'
            
        if letters and not lowercase:
            if search('[a-z]+', password):
                return False, 'Password does contain lower case letters'

        if letters and uppercase:
            if not search('[A-Z]+', password):
                return False, 'Password does not contain upper case letters'
            if not recurring_type_allowed:
                if search('[A-Z]{2}+', password):
                    return False, 'Password does contain recurring type char - upper case letters'
            
        if letters and not uppercase:
            if search('[A-Z]+', password):
                return False, 'Password does contain upper case letters'

        if not letters:
            if search('[a-zA-Z]+', password):
                return False, 'Password does contain letters'

        if digits:
            if not search('[0-9]+', password):
                return False, 'Password does not contain digits'            
            if not recurring_type_allowed:
                if search('[0-9]{2}+', password):
                    return False, 'Password does contain recurring type char - digits'
        else:
            if search('[0-9]+', password):
                return False, 'Password does contain digits'

        if punctuation:
            if not search('[' + ascii_punctuations + ']+', password):
                return False, 'Password does not contain punctuations'
            
            if not recurring_type_allowed:
                if search('[' + ascii_punctuations + ']{2}+', password):
                    return False, 'Password does contain recurring type char - punctuations'
        else:
            if search('[' + ascii_punctuations + ']+', password):
                return False, 'Password does contain punctuations'

        return True, 'Password is valid'




# Class functionality test
if __name__ == "__main__":
    password1 = Password.generate(8, 12, True, True, True, True, True, True)
    password2 = Password.generate(8, 12, True, True, True, True, True, False)
    password3 = Password.generate(8, 8, False, True, False, True, True, False)
    password4 = Password.generate(8, 8, True, True, True, True, False, False)
    
    assert Password.validate(password1, 8, 12, True, True, True, True, True, True)[0] == True
    assert Password.validate(password2, 8, 12, True, True, True, True, True, False)[0] == True
    assert Password.validate(password4, 8, 8, False, True, False, True, True, False)[0] == False
    assert Password.validate(password3, 8, 8, True, True, True, True, False, False)[0] == False