package com.ftnet;

import net.floodlightcontroller.core.IFloodlightProviderService;
import net.floodlightcontroller.core.IOFSwitch;
import net.floodlightcontroller.core.module.FloodlightModuleContext;
import net.floodlightcontroller.core.module.FloodlightModuleException;
import net.floodlightcontroller.core.module.IFloodlightModule;
import net.floodlightcontroller.core.module.IFloodlightService;
import org.openflow.protocol.OFType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class FTManager implements IFloodlightModule {

    protected static Logger log = LoggerFactory.getLogger(FTManager.class.getSimpleName());
    private final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
    private ArrayList<String> connectedHosts;
//    private HashMap<String, Socket>connectedHosts;

    private IOFSwitch iofSwitch;
    private IFloodlightProviderService floodlightProvider;
    OFListener ofListener;


    /**
     * Return the list of interfaces that this module implements.
     * All interfaces must inherit IFloodlightService
     *
     * @return
     */
    @Override
    public Collection<Class<? extends IFloodlightService>> getModuleServices() {
        return null;
    }

    /**
     * Instantiate (as needed) and return objects that implement each
     * of the services exported by this module.  The map returned maps
     * the implemented service to the object.  The object could be the
     * same object or different objects for different exported services.
     *
     * @return The map from service interface class to service implementation
     */
    @Override
    public Map<Class<? extends IFloodlightService>, IFloodlightService> getServiceImpls() {
        return null;
    }

    /**
     * Get a list of Modules that this module depends on.  The module system
     * will ensure that each these dependencies is resolved before the
     * subsequent calls to init().
     *
     * @return The Collection of IFloodlightServices that this module depends
     * on.
     */
    @Override
    public Collection<Class<? extends IFloodlightService>> getModuleDependencies() {
        Collection<Class<? extends IFloodlightService>> l =
                new ArrayList<Class<? extends IFloodlightService>>();
        l.add(IFloodlightProviderService.class);
        return l;
    }

    /**
     * This is a hook for each module to do its <em>internal</em> initialization,
     * e.g., call setService(context.getService("Service"))
     * <p>
     * All module dependencies are resolved when this is called, but not every module
     * is initialized.
     *
     * @param context
     * @throws FloodlightModuleException
     */
    @Override
    public void init(FloodlightModuleContext context) throws FloodlightModuleException {
        floodlightProvider = context.getServiceImpl(IFloodlightProviderService.class);
        ofListener = new OFListener(this);
        connectedHosts = new ArrayList<>();
    }

    void addHost(String ipAddr) {
        if(!connectedHosts.contains(ipAddr)) {
            log.info("Adding new host " + ipAddr);
            this.connectedHosts.add(ipAddr);
            log.info("Current hosts: " + connectedHosts);
        }
    }


    ArrayList<String> getHosts() {
        return this.connectedHosts;
    }

    void setSwitch(IOFSwitch sw) {
        log.debug("Switch set in");
        this.iofSwitch = sw;
    }
    IOFSwitch getSwitch() { return this.iofSwitch; }

    void startMonitoring() {
        scheduler.schedule(new HostMonitor(this),2, TimeUnit.SECONDS);
    }
    void startListening() {
        scheduler.schedule(new ClientListener(this),2, TimeUnit.SECONDS);
    }


    /**
     * This is a hook for each module to do its <em>external</em> initializations,
     * e.g., register for callbacks or query for state in other modules
     * <p>
     * It is expected that this function will not block and that modules that want
     * non-event driven CPU will spawn their own threads.
     *
     * @param context
     */
    @Override
    public void startUp(FloodlightModuleContext context) {

        this.addHost("192.168.1.1");
        this.addHost("192.168.1.2");
        this.addHost("192.168.1.3");

        startMonitoring();
        startListening();
        floodlightProvider.addOFMessageListener(OFType.PACKET_IN, ofListener);
        floodlightProvider.addOFSwitchListener(ofListener);
    }
}
