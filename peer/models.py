from django.db import models
from noc.lib.validators import check_asn
from noc.lib.tt import tt_url

class LIR(models.Model):
    class Admin: pass
    class Meta:
        verbose_name="LIR"
        verbose_name_plural="LIRs"
    name=models.CharField("LIR name",unique=True,maxlength=64)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return unicode(self.name)

class AS(models.Model):
    class Admin:
        list_display=["asn","description","lir"]
        list_filter=["lir"]
        search_fields=["asn","description"]
    class Meta:
        verbose_name="AS"
        verbose_name_plural="ASes"
    lir=models.ForeignKey(LIR,verbose_name="LIR")
    asn=models.IntegerField("ASN",unique=True,validator_list=[check_asn])
    description=models.CharField("Description",maxlength=64)
    rpsl_header=models.TextField("RPSL Header",null=True,blank=True)
    rpsl_footer=models.TextField("RPSL Footer",null=True,blank=True)
    def __str__(self):
        return "AS%d (%s)"%(self.asn,self.description)
    def __unicode__(self):
        return u"AS%d (%s)"%(self.asn,self.description)
    def _rpsl(self):
        s=[p.rpsl for p in self.peer_set.all()]
        return "\n".join(s)
    rpsl=property(_rpsl)

class PeeringPointType(models.Model):
    class Admin:
        list_display=["name"]
    class Meta:
        verbose_name="Peering Point Type"
        verbose_name_plural="Peering Point Types"
    name=models.CharField("Name",maxlength=32,unique=True)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return unicode(self.name)

class PeeringPoint(models.Model):
    class Admin:
        list_display=["hostname","management_ip","type"]
        list_filter=["type"]
        search_fields=["hostname","management_ip"]
    class Meta:
        verbose_name="Peering Point"
        verbose_name_plural="Peering Points"
    hostname=models.CharField("FQDN",maxlength=64,unique=True)
    management_ip=models.IPAddressField("IP",unique=True)
    type=models.ForeignKey(PeeringPointType,verbose_name="Type")
    def __str__(self):
        return self.hostname
    def __unicode__(self):
        return unicode(self.hostname)

class PeerGroup(models.Model):
    class Admin:
        list_display=["name","description"]
    class Meta:
        verbose_name="Peer Group"
        verbose_name_plural="Peer Groups"
    name=models.CharField("Name",maxlength=32,unique=True)
    description=models.CharField("Description",maxlength=64,unique=True)
    def __str__(self):
        return self.name
    def __unicode__(self):
        return unicode(self.name)
        
class Peer(models.Model):
    class Admin:
        list_display=["peering_point","local_asn","remote_asn","import_filter","export_filter","local_ip","remote_ip","description"]
        search_fields=["remote_asn","description"]
        list_filter=["peering_point"]
    class Meta:
        verbose_name="Peer"
        verbose_name_plural="Peers"
    peer_group=models.ForeignKey(PeerGroup,verbose_name="Peer Group")
    peering_point=models.ForeignKey(PeeringPoint,verbose_name="Peering Point")
    local_asn=models.ForeignKey(AS,verbose_name="Local AS")
    local_ip=models.IPAddressField("Local IP")
    remote_asn=models.IntegerField("Remote AS")
    remote_ip=models.IPAddressField("Remote IP")
    import_filter=models.CharField("Import filter",maxlength=64)
    local_pref=models.IntegerField("Local Pref",null=True,blank=True)
    export_filter=models.CharField("Export filter",maxlength=64)
    description=models.CharField("Description",maxlength=64,null=True,blank=True)
    tt=models.IntegerField("TT",blank=True,null=True)
    def _tt_url(self):
        return tt_url(self)
    tt_url=property(_tt_url)
    def _rpsl(self):
        s="import:          from AS%d"%self.remote_asn
        if self.local_pref:
            s+=" action pref=%d;"%self.local_pref
        s+=" accept %s\n"%self.import_filter
        s+="export:          to AS%s announce %s"%(self.remote_asn,self.export_filter)
        return s
    rpsl=property(_rpsl)