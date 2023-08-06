from panda3d.core import NodePath, Vec4, Texture

from direct.actor.Actor import Actor

from toontown_utils import TemplateManager

from toontown_utils.toon.ToonSpecies import ToonSpecies
from toontown_utils.toon.ToonPart import ToonPart
from toontown_utils.toon.ToonHead import ToonHead, Eyelashes


class ToonActor(Actor):
    def __init__(self, species: ToonSpecies | str, head: str | ToonHead, torso: str | ToonPart, legs: ToonPart | str,
                 clothingType: str = "skirt", eyelashes: bool = False) -> None:
        Actor.__init__(self)
        if isinstance(species, str):
            species = TemplateManager.Species[species]

        if isinstance(torso, str):
            torso = TemplateManager.getTorso(torso, clothingType)

        if isinstance(legs, str):
            legs = TemplateManager.getLegs(legs, clothingType)

        self.headType = species.heads[head]
        self.torsoType = torso
        self.legsType = legs

        self.head: NodePath = None
        self.muzzles: dict[str, NodePath] = {}
        self.leftPupil: NodePath = None
        self.rightPupil: NodePath = None

        self.torso: NodePath = None
        self.legs: NodePath = None

        self.createModel(species, self.headType, self.torsoType, self.legsType, eyelashes)

    def createModel(self, species: ToonSpecies, head: ToonHead, torso: ToonPart, legs: ToonPart, eyelashes: bool) -> None:
        self.createHead(head, eyelashes)
        self.createTorso(torso)
        self.createLegs(legs)
        self.setScale(species.size)

    def createLegs(self, legsPart: ToonPart) -> None:
        self.loadModel(legsPart.model, "legs")
        self.loadAnims(legsPart.anims, "legs")
        self.legs = self.getPart("legs")

        self.legs.find("**/shoes").stash()
        self.legs.find("**/boots_short").stash()
        self.legs.find("**/boots_long").stash()

        if self.torso is not None:
            self.torso.reparentTo(self.legs.find("**/joint_hips"))

    def createTorso(self, torsoPart: ToonPart) -> None:
        self.loadModel(torsoPart.model, "torso")
        self.loadAnims(torsoPart.anims, "torso")
        self.torso = self.getPart("torso")

        if self.legs is not None:
            self.torso.reparentTo(self.legs.find("**/joint_hips"))
        if self.head is not None:
            self.head.reparentTo(self.torso.find("**/def_head"))

    def createHead(self, head: ToonHead, eyelashes: bool = False) -> None:
        # TODO: maybe remove nodes instead of stashing them
        self.loadModel(head.model, "head")
        if head.anims is not None:
            self.loadAnims(head.anims, "head")
        self.head: NodePath = self.getPart("head")

        if not head.keepAllParts:
            # TODO: dirty fix, do this better
            if self.head.getNumChildren() > 1:
                self.head.getChildren().stash()
            else:
                self.head.getChildren()[0].getChildren().stash()
            if head.keepParts is not None:
                for part in head.keepParts:
                    partNode: NodePath = self.head.find(f"**/{part};+s")
                    if partNode.isEmpty():
                        continue
                    partNode.unstash()

        for part in head.colorParts:
            partNode: NodePath = self.head.find(f"**/{part};+s")
            if partNode.isEmpty():
                continue
            partNode.unstash()

        self.leftPupil = self.head.find(f"**/{head.leftPupil};+s")
        self.leftPupil.unstash()
        self.rightPupil = self.head.find(f"**/{head.rightPupil};+s")
        self.rightPupil.unstash()
        self.head.find(f"**/{head.eyes};+s").unstash()

        self.createMuzzles(head)

        if eyelashes:
            self.createEyelashes(head.eyelashes)

        if self.torso is not None:
            self.head.reparentTo(self.torso.find("**/def_head"))

    def createEyelashes(self, lashes: Eyelashes) -> None:
        if lashes.model:
            eyelashes = loader.loadModel(lashes.model)
            eyelashes.getChildren()[0].getChildren().stash()
            eyelashes.find(f"**/{lashes.open};+s").unstash()
            eyelashes.reparentTo(self.head)
        else:
            self.head.find(f"**/{lashes.closed};+s").stash()

    def createMuzzles(self, head: ToonHead) -> None:
        self.muzzles = {}
        if head.muzzles is not None:
            for muzzle, part in head.muzzles.items():
                muzzleNode: NodePath = self.head.find(f"**/{part};+s")
                self.muzzles[muzzle] = muzzleNode
                muzzleNode.stash()

        if head.extraMuzzles is not None:
            for model, muzzles in head.extraMuzzles.items():
                node: NodePath = loader.loadModel(model)
                node.getChildren()[0].getChildren().stash()
                node.reparentTo(self.head)
                for muzzle, part in muzzles.items():
                    self.muzzles[muzzle] = node.find(f"**/{part};+s")

        self.muzzles["neutral"].unstash()

    def showMuzzle(self, muzzle: str) -> None:
        for node in self.muzzles.values():
            node.stash()
        self.muzzles[muzzle].unstash()

    def setEyesTexture(self, tex: Texture) -> None:
        self.head.find(f"**/{self.headType.eyes}").setTexture(tex, 1)

    def setLegsColor(self, color: Vec4) -> None:
        for pieceName in ("legs", "feet"):
            piece = self.legs.find(f"**/{pieceName}")
            piece.setColor(color)

    def setTorsoColor(self, color: Vec4) -> None:
        for pieceName in ("arms", "neck"):
            piece = self.torso.find(f"**/{pieceName}")
            piece.setColor(color)

    def setHeadColor(self, color: Vec4) -> None:
        for partName in self.headType.colorParts:
            part: NodePath = self.head.find(f"**/{partName}")
            if part.isEmpty():
                continue
            part.setColor(color)

    def setGlovesColor(self, color: Vec4) -> None:
        gloves = self.torso.find("**/hands")
        gloves.setColor(color)

    def setTopColor(self, color: Vec4) -> None:
        for pieceName in ("torso-top", "sleeves"):
            piece = self.legs.find(f"**/{pieceName}")
            piece.setColor(color)

    def setBottomColor(self, color: Vec4) -> None:
        piece = self.legs.find("**/torso-bot")
        piece.setColor(color)

    def setBottomTexture(self, tex: Texture | str) -> None:
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self.torso.find("**/torso-bot").setTexture(tex, 1)

    def setTopTexture(self, tex: Texture | str) -> None:
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self.torso.find("**/torso-top").setTexture(tex, 1)

    def setSleeveTexture(self, tex: Texture | str) -> None:
        if not isinstance(tex, Texture):
            tex = loader.loadTexture(tex)
        self.torso.find("**/sleeves").setTexture(tex, 1)
