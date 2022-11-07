import pygame, os, json, random, math
from pygame.locals import *

class UIElements():
    def __init__(self):
        self.__array = []

    def find(self, name):
        for each in self.__array:
            if each.name == name:
                return each
        return None

    def append(self, element):
        self.__array.append(element)

    def visible(self):
        found = []
        for element in self.__array:
            if element.getVisible():
                found.append(element)
        return found

class UIElement():
    def __init__(self, width, height, visible, name):
        self.__boundingBox = Rect(0, 0, width, height)
        self.__visible = visible
        self.name = name
        self.text = ''

        uiElements.append(self)

    def moveTo(self, x, y):
        self.__boundingBox.x = x
        self.__boundingBox.y = y

    def setVisible(self, a):
        self.__visible = a

    def getVisible(self):
        return self.__visible

    def getBoundingBox(self):
        return self.__boundingBox

class Entities():
    def __init__(self):
        self.__array = []

    def find(self, name):
        for each in self.__array:
            if each.name == name:
                return each
        return None

    def findAll(self, name):
        found = []
        for each in self.__array:
            if each.name == name:
                found.append(each)
        return found

    def append(self, entity):
        self.__array.append(entity)

    def visible(self):
        found = []
        for entity in self.__array:
            if entity.getVisible():
                found.append(entity)
        return found

class Entity():
    def __init__(self, width, height, visible, name):
        self.__visible = visible
        self.name = name

        name = name.lower().replace(' ', '_')
        try:
            self.image = pygame.image.load(os.path.join('images', 'enemies', name + '.png'))
            dimensions = self.image.get_size()
            if dimensions[1] > uiElements.find('EnemyContainer').getBoundingBox().height:
                multi = uiElements.find('EnemyContainer').getBoundingBox().height / dimensions[1]
                self.image = pygame.transform.scale(self.image, (math.floor(dimensions[0] * multi), uiElements.find('EnemyContainer').getBoundingBox().height))
        except pygame.error:
            try:
                self.image = pygame.image.load(os.path.join('images', 'characters', name + '.png'))
                dimensions = self.image.get_size()
                if dimensions[1] > uiElements.find('EnemyTopContainer').getBoundingBox().height:
                    multi = uiElements.find('EnemyTopContainer').getBoundingBox().height / dimensions[1]
                    self.image = pygame.transform.scale(self.image, (math.floor(dimensions[0] * multi), uiElements.find('EnemyTopContainer').getBoundingBox().height))
            except pygame.error:
                #assume no image was found
                self.image = None

        if width == 0 and height == 0 and self.image != None:
            dimensions = self.image.get_size()
            self.__boundingBox = Rect(0, 0, dimensions[0], dimensions[1])
        else:
            self.__boundingBox = Rect(0, 0, width, height)

        entities.append(self)

    def moveBy(self, xOffset, yOffset):
        self.__boundingBox = self.__boundingBox.move(xOffset, yOffset)

    def moveTo(self, x, y):
        self.__boundingBox.x = x
        self.__boundingBox.y = y

    def inflateBy(self, xOffset, yOffset):
        self.__boundingBox = self.__boundingBox.inflate(xOffset, yOffset)

    def setVisible(self, a):
        self.__visible = a

    def getVisible(self):
        return self.__visible

    def getBoundingBox(self):
        return self.__boundingBox


class Enemy(Entity):
    def __init__(self, width, height, visible, name, facing, level, hp, melee, ranged, potential, evasion, attacks):
        Entity.__init__(self, width, height, visible, name)
        self.__facing = facing
        self.__level = level
        self.__hp = hp
        self.__currentHp = hp
        self.__melee = melee
        self.__ranged = ranged
        self.__potential = potential
        self.__evasion = evasion
        self.__attacks = attacks

    def modifyCurrentHp(self, value):
        self.__currentHp = self.__currentHp + value

    def getLevel(self):
        return self.__level

    def getFacing(self):
        return self.__facing

class Character(Entity):
    def __init__(self, width, height, visible, name, level, hp, melee, ranged, potential, evasion, arts, meleeWeapon, rangedWeapon):
        Entity.__init__(self, width, height, visible, name)
        #character stats
        self.__level = level
        self.__hp = hp
        self.__melee = melee
        self.__ranged = ranged
        self.__potential = potential
        self.__evasion = evasion
        self.__arts = arts
        #these are Weapon objects
        self.__meleeWeapon = meleeWeapon
        self.__rangedWeapon = rangedWeapon
        #variables
        self.__timeOfLastAutoAttack = 0.0

    def getLevel(self):
        return self.__level

    def dealDamage(self, weaponType, target):
        if weaponType == 'melee':
            weapon = self.__meleeWeapon
            charAmount = self.__melee
        elif weaponType == 'ranged':
            weapon = self.__rangedWeapon
            charAmount = self.__ranged
        dmgAmount = weapon.attack
        stabVar = random.randint(-weapon.stability, weapon.stability)
        dmgAmount += stabVar
        if dmgAmount < 1:
            dmgAmount = 1
        dmgAmount += charAmount / 10
        dmgAmount = dmgAmount * (1.0 + self.__potential / 100)
        dmgAmount = round(dmgAmount, 0)
        #inflict damage amount on target
        target.modifyCurrentHp(dmgAmount)

class Weapon(Entity):
    def __init__(self, width, height, visible, name, type, category, attack, minLevel, cooldown, tpGain, stability, upgrades):
        Entity.__init__(self, width, height, visible, name)
        self.__type = type
        self.__category = category
        self.attack = attack
        self.__minLevel = minLevel
        self.cooldown = cooldown
        self.tpGain = tpGain
        self.stability = stability
        self.__upgrades = upgrades

def TestVariableExists(varToTest):
    try:
        type(varToTest)
        return True
    except NameError:
        return False

def Update():
    clock.tick(FRAMERATE)

    playerCharacter = entities.find('Elma')
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            #attributes: key, mod, unicode, scancode
            print(event)
        elif event.type == MOUSEBUTTONDOWN:
            #attributes: pos, button
            print(event.button)
            print(event.pos)
            if event.button == 1: #left mouse
                if uiElements.find('EnemyTopContainer').getBoundingBox().collidepoint(event.pos):
                    playerCharacter.getBoundingBox().center = uiElements.find('EnemyTopContainer').getBoundingBox().center
                elif uiElements.find('EnemyLeftContainer').getBoundingBox().collidepoint(event.pos):
                    playerCharacter.getBoundingBox().center = uiElements.find('EnemyLeftContainer').getBoundingBox().center
                elif uiElements.find('EnemyRightContainer').getBoundingBox().collidepoint(event.pos):
                    playerCharacter.getBoundingBox().center = uiElements.find('EnemyRightContainer').getBoundingBox().center
                elif uiElements.find('EnemyBottomContainer').getBoundingBox().collidepoint(event.pos):
                    playerCharacter.getBoundingBox().center = uiElements.find('EnemyBottomContainer').getBoundingBox().center
        else:
            #print(event)
            pass

    Draw()

def Draw():
    screen.fill((255, 255, 255))

    for element in uiElements.visible():
        pygame.draw.rect(screen, (0, 0, 0), element.getBoundingBox(), 2)
        if element.text != '':
            s = fontMedium.render(element.text, True, (0,0,0))
            screen.blit(s, element.getBoundingBox())

    for entity in entities.visible():
        #pygame.draw.rect(screen, (255, 0, 0), entity.getBoundingBox())
        screen.blit(entity.image, entity.getBoundingBox())

    pygame.display.update()

def GenerateEnemy(enemiesTemplate):
    print('run generate enemy')
    i = random.randint(0, len(enemiesTemplate) - 1)
    template = enemiesTemplate[i]
    #calculate level
    level = random.randint( template["levelMin"], template["levelMax"] )
    levelDifference = template["levelMax"] - template["levelMin"]
    levelsAboveMin = level - template["levelMin"]
    #calculate hp
    hpDifference = template["hpMax"] - template["hpMin"]
    hpPer = hpDifference // levelDifference
    hp = template["hpMin"] + (hpPer * levelsAboveMin)
    #calculate melee
    meleeDifference = template["meleeMax"] - template["meleeMin"]
    meleePer = meleeDifference // levelDifference
    melee = template["meleeMin"] + (meleePer * levelsAboveMin)
    #calculate ranged
    rangedDifference = template["rangedMax"] - template["rangedMin"]
    rangedPer = rangedDifference // levelDifference
    ranged = template["rangedMin"] + (rangedPer * levelsAboveMin)
    #calculate potential
    potentialDifference = template["potentialMax"] - template["potentialMin"]
    potentialPer = potentialDifference // levelDifference
    potential = template["potentialMin"] + (potentialPer * levelsAboveMin)
    #calculate evasion
    evasionDifference = template["evasionMax"] - template["evasionMin"]
    evasionPer = evasionDifference // levelDifference
    evasion = template["evasionMin"] + (evasionPer * levelsAboveMin)

    #width, height, visible, name, facing, level, hp, melee, ranged, potential, evasion, attacks
    enemy = Enemy(0, 0, True, template["name"], template["facing"], level, hp, melee, ranged, potential, evasion, template["attacks"])
    return enemy

def GenerateCharacter(charactersTemplate, weaponsTemplate):
    print('run generate character')
    i = random.randint(0, len(charactersTemplate) - 1)
    template = charactersTemplate[i]
    #calculate level
    level = template["level"]
    #calculate hp
    hp = template["hp"]
    #calculate melee
    melee = template["melee"]
    #calculate ranged
    ranged = template["ranged"]
    #calculate potential
    potential = template["potential"]
    #calculate evasion
    evasion = template["evasion"]
    #create weapon object
    meleeWeapon = LoadInWeapon(template['meleeWeapon'], weaponsTemplate)
    rangedWeapon = LoadInWeapon(template['rangedWeapon'], weaponsTemplate)

    #width, height, visible, name, level, hp, melee, ranged, potential, evasion, arts
    character = Character(0, 0, True, template["name"], level, hp, melee, ranged, potential, evasion, template["arts"], meleeWeapon, rangedWeapon)
    return character

def LoadInWeapon(name, weaponsTemplate):
    print('run load in weapon with name=' + str(name))
    for i in range(0, len(weaponsTemplate)):
        if weaponsTemplate[i]['name'] == name:
            template = weaponsTemplate[i]
            break
    if not TestVariableExists(template):
        print('weapon to load not found in json file')
        return None
    
    #width, height, visible, name, type, category, attack, minLevel, cooldown, tpGain, stability, upgrades
    weapon = Weapon(0, 0, False, template['name'], template['type'], template['category'], template['attack'], template['minLevel'], template['cooldown'], template['tpGain'], template['stability'], template['upgrades'])
    return weapon

def InitiateBattle(enemiesTemplate, charactersTemplate, weaponsTemplate):
    print('run initiate battle')
    #create and position enemy
    enemy = GenerateEnemy(enemiesTemplate)
    enemy.getBoundingBox().center = uiElements.find('EnemyContainer').getBoundingBox().center
    #create and position player character
    character = GenerateCharacter(charactersTemplate, weaponsTemplate)
    character.getBoundingBox().center = uiElements.find('EnemyTopContainer').getBoundingBox().center

    #set UI text
    uiElements.find('EnemyContainer').text = enemy.name + ' (' + str(enemy.getLevel()) + ')'
    if enemy.getFacing() == 0:
        uiElements.find('EnemyTopContainer').text = 'FRONT'
        uiElements.find('EnemyLeftContainer').text = 'SIDE'
        uiElements.find('EnemyRightContainer').text = 'SIDE'
        uiElements.find('EnemyBottomContainer').text = 'BACK'
    elif enemy.getFacing() == 1:
        uiElements.find('EnemyTopContainer').text = 'SIDE'
        uiElements.find('EnemyLeftContainer').text = 'BACK'
        uiElements.find('EnemyRightContainer').text = 'FRONT'
        uiElements.find('EnemyBottomContainer').text = 'SIDE'
    elif enemy.getFacing() == 2:
        uiElements.find('EnemyTopContainer').text = 'BACK'
        uiElements.find('EnemyLeftContainer').text = 'SIDE'
        uiElements.find('EnemyRightContainer').text = 'SIDE'
        uiElements.find('EnemyBottomContainer').text = 'FRONT'
    elif enemy.getFacing() == 3:
        uiElements.find('EnemyTopContainer').text = 'SIDE'
        uiElements.find('EnemyLeftContainer').text = 'FRONT'
        uiElements.find('EnemyRightContainer').text = 'BACK'
        uiElements.find('EnemyBottomContainer').text = 'SIDE'

def BuildArenaUI():
    arenaContainer = UIElement(720, 720, True, 'ArenaContainer' )
    arenaBoundingBox = arenaContainer.getBoundingBox()
    arenaCenter = arenaBoundingBox.center
    enemyContainer = UIElement(450, 450, True, 'EnemyContainer')
    enemyContainer.getBoundingBox().center = arenaCenter

    enemyTopContainer = UIElement(135, 135, True, 'EnemyTopContainer')
    enemyTopContainer.getBoundingBox().centerx = arenaCenter[0]

    enemyLeftContainer = UIElement(135, 135, True, 'EnemyLeftContainer')
    enemyLeftContainer.getBoundingBox().centery = arenaCenter[1]

    enemyRightContainer = UIElement(135, 135, True, 'EnemyRightContainer')
    enemyRightContainer.getBoundingBox().midright = arenaBoundingBox.midright

    enemyBottomContainer = UIElement(135, 135, True, 'EnemyBottomContainer')
    enemyBottomContainer.getBoundingBox().midbottom = arenaBoundingBox.midbottom

def Main():
    print('run main function')
    #build UI
    BuildArenaUI()

    #instantiate game data
    #load and decode enemies file
    file = open('enemies.json', 'r')
    enemiesTemplate = json.load(file)
    file.close()
    #load and decode characters file
    file = open('characters.json', 'r')
    charactersTemplate = json.load(file)
    file.close()
    #load and decode weapons file
    file = open('weapons.json', 'r')
    weaponsTemplate = json.load(file)
    file.close()

    InitiateBattle(enemiesTemplate, charactersTemplate, weaponsTemplate)

    while True:
        Update()

if __name__ == "__main__":
    print('run main global setup')
    #pygame initialisation and display setup
    pygame.init()
    pygame.display.set_caption('Xenoblade JRPG')

    #declare global CONSTANTS
    FRAMERATE = 120
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    #declare global variables
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    entities = Entities()
    uiElements = UIElements()
    fontSmall = pygame.font.SysFont('Arial', 14)
    fontMedium = pygame.font.SysFont('Arial', 24)

    Main()